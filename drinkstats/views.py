from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import DBAPIError
from sqlalchemy import func
import datetime
import time
from .models import DBSession, DropLog, DrinkItem
import drink_log
import money_log
import machines

#-------------------------- API -------------------------------------

@view_config(route_name='api_pop_hours', renderer='json')
def api_pop_hours(request):
    """
    Gets the number of drinks per hour for the given time range
    """
    start_date, end_date = get_timerange(request)
    if 'machine_id' in request.params:
        return drink_log.top_hours(machine_id = request.params['machine_id'])
    elif 'username' in request.params:
        return drink_log.top_hours(username = request.params['username'])
    else:
        return drink_log.top_hours(start_date = start_date, end_date = end_date)

@view_config(route_name='api_item_usage', renderer='json')
def api_item_usage(request):
    """
    Gets the item usage for the specified drink
    """
    item_id = int(request.matchdict['item_id'])
    return drink_log.get_item_usage(item_id)

@view_config(route_name='api_total_usage', renderer='json')
def api_total_usage(request):
    return drink_log.get_total_usage()

@view_config(route_name='api_user_usage', renderer='json')
def api_user_usage(request):
    username = request.matchdict['username']
    return drink_log.get_user_usage(username)

@view_config(route_name='api_machine_usage', renderer='json')
def api_machine_usage(request):
    machine_id = int(request.matchdict['machine_id'])
    return drink_log.get_machine_usage(machine_id)

@view_config(route_name='api_punchcard', renderer='json')
def api_punchcard(request):
    """
    Used by the Github style punchcard graph on the index page
    """
    def parse(x):
        return {'y': x[0] + 1, 'x': 3600000  * x[1], 'amount': x[2],
                'format': x[4], 'marker': {'radius': x[3]}}

    begin = {'x': 0, 'y': 0, 'amount': 0, 'marker': {'radius': 0}}
    end = {'x': 0, 'y': 8, 'amount': 0, 'marker': {'radius': 0}}
    start_date, end_date = get_timerange(request)
    return [begin] + map(parse, drink_log.punchcard(start_date = start_date, end_date = end_date)) + [end]


@view_config(route_name='api_top_drops', renderer='json')
def api_top_drops(request):
    """
    Used by the pie graph on the index page
    """
    def parse(x):
        return {'name': x[1], 'y': x[0], 'url': '/drink/%s' % x[2]}
    if 'machine_id' in request.params:
        return map(parse, drink_log.top_drinks_for_machine(request.params['machine_id'], 15))
    elif 'username' in request.params:
         return map(parse, drink_log.top_drinks(15, request.params['username']))
    else:
        start_date, end_date = get_timerange(request)
        return map(parse, drink_log.top_drinks(15, start_date = start_date, end_date = end_date))


#--------------------------------------------------------------------

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return int(delta.days*86400+delta.seconds+delta.microseconds/1e6)

def get_timerange(request):
    """
    Determines the timerange for the queries
    """
    try:
        start_epoch = request.params['start']
        end_epoch = request.params['end']
        start_date = datetime.datetime.fromtimestamp(int(start_epoch))
        end_date = datetime.datetime.fromtimestamp(int(end_epoch))
    except Exception as e:
        start_date = datetime.datetime(year = 2011, month = 10, day = 17)
        end_date = datetime.datetime.now()
    return start_date, end_date


@view_config(route_name='index', renderer='templates/index.pt')
def index_view(request):
    start_date = end_date = error = None
    if request.method == 'POST':
        if ('cal_year', u'Calendar Year') in request.POST.items():
            end_date = datetime.datetime.now()
            start_date = datetime.datetime(year = end_date.year, month = 1, day = 1)
        elif ('school_year', u'School Year   ') in request.POST.items():
            end_date = datetime.datetime.now()
            if end_date.month >= 8:
                start_date = datetime.datetime(year = end_date.year, month = 8, day = 15)
            else:
                start_date = datetime.datetime(year = end_date.year - 1, month = 8, day = 15)
        elif ('last_month', u' Last Month    ') in request.POST.items():
            end_date = datetime.datetime.now()
            start_date = end_date - datetime.timedelta(days = 30)
        elif ('ever', u'     Ever     ') in request.POST.items():
            start_date = datetime.datetime(year = 2011, month = 10, day = 17)
            end_date = datetime.datetime.now()
        else:
            start_date = datetime.datetime.strptime(request.POST.get('start'), '%m/%d/%Y')
            end_date =  datetime.datetime.strptime(request.POST.get('end'), '%m/%d/%Y')

    if not start_date or not end_date or start_date > end_date:
        start_date = datetime.datetime(year = 2011, month = 10, day = 17)
        end_date = datetime.datetime.now()

    top_spenders = money_log.top_spenders(20, start_date = start_date, end_date = end_date)
    return {'top_users': top_spenders, 'start_date': start_date.strftime('%m/%d/%Y'),
            'end_date': end_date.strftime('%m/%d/%Y'), 'start_date_epoch': unix_time(start_date),
            'end_date_epoch': unix_time(end_date), 'error': error}

@view_config(route_name='drink_page', renderer='templates/drinks.pt')
def drinks_view(request):
    item_id = int(request.matchdict['item_id'])
    return {'item_id': item_id, 'item_name': drink_log.get_item_name(item_id),
            'total_drops': drink_log.get_total_dropped(item_id),
            'top_users_total': drink_log.get_top_users_for_item(item_id),
            'top_users_year': drink_log.get_top_users_for_item_year(item_id)}

@view_config(route_name='user_redirect')
def user_redirect(request):
    username = request.POST.get('username')
    result = drink_log.get_item_id(username)
    if result: # redirect to drink page
        return HTTPFound(location = '/drink/' + str(result[0]))
    if username:
        return HTTPFound(location = 'user/' + username)
    else:
        return HTTPFound(location = '/')

@view_config(route_name='drink_redirect', renderer='templates/users.pt')
def drink_redirect(request):
    username = request.POST.get('username')
    return HTTPFound(location = 'user/' + username)

@view_config(route_name='user_page', renderer='templates/users.pt')
def users_view(request):
    def parse(x):
        return [x[0].strftime('%b, %d, %Y')] + [x[1]] + [x[2]] + [x[3]] + [x[4]]
    username = request.matchdict['username']
    drop_count = drink_log.get_drop_count(username)
    if drop_count:
        return {'username': username, 'hours': drink_log.top_hours(username),
                'top_drinks': drink_log.top_drinks(15, username),
                'drop_count': drop_count, 'error': False,
                'latest_drops': map(parse, drink_log.get_latest_drops(username)),
                'money': money_log.money_spent(username)}
    else:
        return {'message': 'There is no information about ' + username, 'username': '---',
                'error': True}

@view_config(route_name='machine_page', renderer='templates/machine.pt')
def machines_view(request):
    machine_id = int(request.matchdict['machine_id'])
    machine_name = machines.get_machine_name(machine_id)
    top_drops = drink_log.top_drinks_for_machine(machine_id, limit = 15)
    return {'top_drops': top_drops, 'machine_id': machine_id,
            'machine_name': machine_name}

@view_config(route_name='autocomplete', renderer='json')
def autocomplete(request):
    return [item[0] for item in drink_log.get_search_results(request.GET.get('term'))]


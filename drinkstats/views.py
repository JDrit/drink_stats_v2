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
   return {'pop_hours': drink_log.popular_hours()}

@view_config(route_name='api_item_usage', renderer='json')
def api_item_usage(request):
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

#--------------------------------------------------------------------

@view_config(route_name='index', renderer='templates/index.pt')
def index_view(request):
    start_date = datetime.datetime(year = 2011, month = 10, day = 17)
    end_date = datetime.datetime.now()

    error = None
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

    top_drinks = drink_log.top_drinks(15, start_date = start_date, end_date = end_date)
    top_spenders = money_log.top_spenders(15, start_date = start_date, end_date = end_date)
    hours = drink_log.top_hours(start_date = start_date, end_date = end_date)
    punchcard = drink_log.punchcard(start_date = start_date, end_date = end_date)
    print punchcard
    start_date_format = start_date.strftime('%m/%d/%Y')
    end_date_format = end_date.strftime('%m/%d/%Y')
    return {'top_drinks': top_drinks, 'hours': hours,
            'top_users': top_spenders, 'start_date': start_date_format,
            'end_date': end_date_format, 'error': error, 'new_hours': punchcard}

@view_config(route_name='drink_page', renderer='templates/drinks.pt')
def drinks_view(request):
    item_id = int(request.matchdict['item_id'])
    item_name = drink_log.get_item_name(item_id)
    top_users_total = drink_log.get_top_users_for_item(item_id)
    top_users_year = drink_log.get_top_users_for_item_year(item_id)
    total_drops = drink_log.get_total_dropped(item_id)
    return {'item_id': item_id, 'item_name': item_name,
            'total_drops': total_drops,
            'top_users_total': top_users_total,
            'top_users_year': top_users_year}

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

@view_config(route_name='user_page', renderer='templates/users.pt')
def users_view(request):
    username = request.matchdict['username']
    drop_count = drink_log.get_drop_count(username)
    if drop_count:
        return {'username': username, 'hours': drink_log.top_hours(username),
                'top_drinks': drink_log.top_drinks(15, username),
                'drop_count': drop_count, 'error': False,
                'latest_drops': drink_log.get_latest_drops(username)}
    else:
        return {'message': 'There is no information about ' + username,
                'error': True}

@view_config(route_name='machine_page', renderer='templates/machine.pt')
def machines_view(request):
    machine_id = int(request.matchdict['machine_id'])
    machine_name = machines.get_machine_name(machine_id)
    top_drinks = drink_log.top_drinks_for_machine(machine_id)
    top_hours = drink_log.top_hours(machine_id = machine_id)
    return {'top_drops': top_drinks, 'hours': top_hours,
            'machine_id': machine_id, 'machine_name': machine_name}

@view_config(route_name='autocomplete', renderer='json')
def autocomplete(request):
    return [item[0] for item in drink_log.get_search_results(request.GET.get('term'))]


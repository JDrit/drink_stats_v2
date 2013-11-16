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



@view_config(route_name='index', renderer='templates/index.pt')
def index_view(request):
    return {'top_drinks': drink_log.top_drinks(15), 'hours': drink_log.top_hours(), 'top_users': money_log.top_spenders(15)}

@view_config(route_name='drink_page', renderer='templates/drinks.pt')
def drinks_view(request):
    item_id = int(request.matchdict['item_id'])
    item_name = drink_log.get_item_name(item_id)
    top_users = drink_log.get_top_users_for_item(item_id)
    total_drops = drink_log.get_total_dropped(item_id)
    return {'item_id': item_id, 'item_name': item_name,
            'total_drops': total_drops, 'top_users': top_users}

@view_config(route_name='user_redirect')
def user_redirect(request):
    username = request.POST.get('username')
    if username:
        return HTTPFound(location = 'user/' + username)
    else:
        return HTTPFound(location = '/')

@view_config(route_name='user_page', renderer='templates/users.pt')
def users_view(request):
    username = request.matchdict['username']
    return {'username': username, 'hours': drink_log.top_hours(username),
            'top_drinks': drink_log.top_drinks(15, username)}

@view_config(route_name='machine_page', renderer='templates/machine.pt')
def machines_view(request):
    machine_id = int(request.matchdict['machine_id'])
    machine_name = machines.get_machine_name(machine_id)
    top_drinks = drink_log.top_drinks_for_machine(machine_id)
    top_hours = drink_log.top_hours(machine_id = machine_id)
    return {'top_drops': top_drinks, 'hours': top_hours, 'machine_id': machine_id, 'machine_name': machine_name}

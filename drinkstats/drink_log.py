from .models import DBSession, DropLog, DrinkItem, Machine
from sqlalchemy import func
from sqlalchemy.sql import or_
from datetime import datetime, timedelta


def get_search_results(search):
    result = DBSession.query(DropLog.username).filter(DropLog.username.ilike('%' + search + '%')).group_by(DropLog.username).all()
    result += DBSession.query(DrinkItem.item_name).filter(DrinkItem.item_name.ilike('%' + search + '%')).group_by(DrinkItem.item_name).all()
    return result

def get_drop_count(username):
    """
    The number of drops that a user has done
    """
    return len(DBSession.query(DropLog).filter(DropLog.username == username).all())

def get_top_users_for_item_year(item_id, limit = 10):
    """
    The users who get the given item the most
    """
    return DBSession.query(DropLog.username, func.count('*')
            ).filter(DropLog.item_id == item_id, DropLog.time > datetime.now() - timedelta(days = 365)
            ).group_by(DropLog.username).order_by('count_1 desc').limit(limit).all()

def get_top_users_for_item(item_id, limit = 10):
    """
    The users who get the given item the most
    """
    return DBSession.query(DropLog.username, func.count('*')
            ).filter(DropLog.item_id == item_id
            ).group_by(DropLog.username).order_by('count_1 desc'
            ).limit(limit).all()

def get_latest_drops(username, limit = 10):
    """
    Gets the latest drops from the machines
    """
    return DBSession.query(DropLog, DrinkItem.item_name, Machine.display_name, Machine.machine_id
            ).filter(DropLog.username == username
            ).join(DrinkItem, DropLog.item_id == DrinkItem.item_id
            ).join(Machine, Machine.machine_id ==  DropLog.machine_id
            ).order_by("drop_log_id desc").limit(limit).all()


def get_item_name(item_id):
    return DBSession.query(DrinkItem.item_name).filter(DrinkItem.item_id == item_id).first()[0]

def get_item_id(item_name):
    return DBSession.query(DrinkItem.item_id).filter(func.lower(DrinkItem.item_name) == func.lower(item_name)).first()

def get_total_dropped(item_id):
    return len(DBSession.query(DropLog).filter(DropLog.item_id == item_id).all())

def top_drinks_for_machine(machine_id, limit = 10):
    top_drinks = DBSession.query(func.count(DropLog.item_id),
            DrinkItem.item_name, DrinkItem.item_id
            ).filter(DropLog.machine_id == machine_id, DrinkItem.item_name != 'test item'
            ).join(DrinkItem, DropLog.item_id == DrinkItem.item_id
            ).group_by(DropLog.item_id
            ).order_by("count_1 desc"
            ).limit(limit).all()
    return top_drinks

def top_drinks(limit = 10, username = None, start_date = None, end_date = None):
    """
    Gets the top items dropped for the given arguments
    Arguments:
        limit: the top number of results to return, default 10
        username: the username to search for, default everyone
        start_date: the start date of the range, default all
        end_date: the end_date of the range, default all
    """
    if start_date and end_date and start_date < end_date:
        if username:
            top_drinks = DBSession.query(func.count(DropLog.item_id),
                    DrinkItem.item_name, DrinkItem.item_id).filter(
                    DropLog.time >= start_date, DropLog.time <= end_date,
                    DropLog.username == username, DrinkItem.item_name != 'test item'
                    ).join(DrinkItem,DropLog.item_id == DrinkItem.item_id
                    ).group_by(DropLog.item_id).order_by("count_1 desc"
                    ).limit(limit).all()
        else:
            top_drinks = DBSession.query(func.count(DropLog.item_id),
                    DrinkItem.item_name, DrinkItem.item_id).filter(
                    DropLog.time >= start_date, DropLog.time <= end_date, DrinkItem.item_name != 'test item'
                    ).join(DrinkItem,DropLog.item_id == DrinkItem.item_id
                    ).group_by(DropLog.item_id).order_by("count_1 desc"
                    ).limit(limit).all()

    else:
        if username:
            top_drinks = DBSession.query(func.count(DropLog.item_id),
                DrinkItem.item_name, DrinkItem.item_id).filter(
                DropLog.username == username, DrinkItem.item_name != 'test item').join(
                DrinkItem, DropLog.item_id == DrinkItem.item_id
                ).group_by(DropLog.item_id).order_by("count_1 desc"
                ).limit(limit).all()

        else:
            top_drinks = DBSession.query(func.count(DropLog.item_id),
                    DrinkItem.item_name, DrinkItem.item_id).filter(
                    DrinkItem.item_name != 'test item'
                    ).join(DrinkItem, DropLog.item_id == DrinkItem.item_id
                    ).group_by(DropLog.item_id).order_by("count_1 desc"
                    ).limit(limit).all()
    return top_drinks

def top_hours(username = None, machine_id = None, start_date = None, end_date = None):
    """
    Gets the number of drops for each hour of the day
    Arguments:
        username: The username to filter by for the results
        machine_id: The ID of the machine to get the drop count for
        start_date: the start date to filter results by
        end_date: the end date to filter results by
    """
    if machine_id: # top hours for a given machine
        if start_date and end_date and start_date <= end_date: # within a time frame
            pop_hours = DBSession.query(
                    func.hour(DropLog.time), func.count("*")
                    ).filter(DropLog.machine_id == machine_id,
                            DropLog.time >= start_date, DropLog.time <= end_date
                    ).group_by(func.hour(DropLog.time)
                    ).order_by(func.hour(DropLog.time)).all()
        else:
            pop_hours = DBSession.query(
                    func.hour(DropLog.time), func.count("*")
                    ).filter(DropLog.machine_id == machine_id
                    ).group_by(func.hour(DropLog.time)
                    ).order_by(func.hour(DropLog.time)).all()
    elif not username: # top hours overall
        if start_date and end_date and start_date <= end_date: # within a time frame
            pop_hours = DBSession.query(
                func.hour(DropLog.time), func.count("*")
                ).filter(DropLog.time >= start_date, DropLog.time <= end_date
                ).group_by(func.hour(DropLog.time)).order_by(
                        func.hour(DropLog.time)).all()
        else: # top hours all time for everyone
            pop_hours = DBSession.query(
                func.hour(DropLog.time), func.count("*")
                ).group_by(func.hour(DropLog.time)).order_by(
                        func.hour(DropLog.time)).all()
    else: # top hours for a user
        if start_date and end_date and start_date <= end_date: # within a time frame
            pop_hours = DBSession.query(
                    func.hour(DropLog.time), func.count("*")
                    ).filter(DropLog.username == username,
                            DropLog.time >= start_date, DropLog.time <= end_date
                    ).group_by(func.hour(DropLog.time)
                    ).order_by(func.hour(DropLog.time)).all()

        else:
            pop_hours = DBSession.query(
                    func.hour(DropLog.time), func.count("*")
                    ).filter(DropLog.username == username
                    ).group_by(func.hour(DropLog.time)
                    ).order_by(func.hour(DropLog.time)).all()

    data = []
    current_hour = 0
    for hour in pop_hours:
        while hour[0] != current_hour:
            data.append(0)
            current_hour += 1
        data.append(hour[1])
        current_hour += 1
    data += [0] * (24 - len(data))
    return data

def get_machine_usage(machine_id):
    entries = DBSession.query(func.count('*'), func.date(DropLog.time)
            ).filter(DropLog.machine_id == machine_id
            ).group_by(func.date(DropLog.time)).all()
    return process_usage(entries)

def get_user_usage(username):
    entries = DBSession.query(func.count('*'), func.date(DropLog.time)
            ).filter(DropLog.username == username
            ).group_by(func.date(DropLog.time)).all()
    return process_usage(entries)

def get_total_usage():
    entries = DBSession.query(func.count('*'), func.date(DropLog.time)
            ).group_by(func.date(DropLog.time)).all()
    return process_usage(entries)

def get_item_usage(item_id):
    entries = DBSession.query(func.count('*'), func.date(DropLog.time)
            ).filter(DropLog.item_id == item_id
            ).group_by(func.date(DropLog.time)).all()
    return process_usage(entries)

def process_usage(entries):
    data = []
    current_date = None
    for entry in entries:
        # puts in values of zeros where there are no entries
        while current_date and entry[1] - current_date > timedelta(days = 1):
            current_date += timedelta(days = 1)
            data.append([int(current_date.strftime('%s')) * 1000, 0])

        data.append([int(entry[1].strftime('%s')) * 1000, entry[0]])
        current_date = entry[1]
    return data

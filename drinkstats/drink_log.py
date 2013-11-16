from .models import DBSession, DropLog, DrinkItem
from sqlalchemy import func
from datetime import datetime, timedelta

def get_top_users_for_item(item_id, limit = 10):
    return DBSession.query(DropLog.username, func.count('*')
            ).filter(DropLog.item_id == item_id
                    ).group_by(DropLog.username).order_by('count_1 desc').limit(limit).all()

def get_item_name(item_id):
    return DBSession.query(DrinkItem.item_name).filter(DrinkItem.item_id == item_id).first()[0];

def get_total_dropped(item_id):
    return len(DBSession.query(DropLog).filter(DropLog.item_id == item_id).all())


def top_users(limit):
    users = DBSession.query()

def top_drinks_for_machine(machine_id, limit = 10):
    top_drinks = DBSession.query(func.count(DropLog.item_id),
            DrinkItem.item_name, DrinkItem.item_id
            ).filter(DropLog.machine_id == machine_id
            ).join(DrinkItem, DropLog.item_id == DrinkItem.item_id
            ).group_by(DropLog.item_id
            ).order_by("count_1 desc"
            ).limit(limit).all()
    return top_drinks

def top_drinks(limit = 10, username = None):
    if not username:
        top_drinks = DBSession.query(func.count(DropLog.item_id),
                DrinkItem.item_name, DrinkItem.item_id).join(DrinkItem,
                        DropLog.item_id == DrinkItem.item_id
                        ).group_by(DropLog.item_id).order_by(
                                "count_1 desc"
                                    ).limit(limit).all()
    else:
        top_drinks = DBSession.query(func.count(DropLog.item_id),
                DrinkItem.item_name, DrinkItem.item_id
                ).filter(DropLog.username == username
                ).join(DrinkItem, DropLog.item_id == DrinkItem.item_id
                ).group_by(DropLog.item_id
                ).order_by("count_1 desc"
                ).limit(limit).all()

    return top_drinks

def top_hours(username = None, machine_id = None):
    if machine_id:
        pop_hours = DBSession.query(
                func.hour(DropLog.time), func.count("*")
                ).filter(DropLog.machine_id == machine_id
                ).group_by(func.hour(DropLog.time)
                ).order_by(func.hour(DropLog.time)).all()
    else:
        if not username:
            pop_hours = DBSession.query(
                    func.hour(DropLog.time), func.count("*")
                    ).group_by(func.hour(DropLog.time)).order_by(
                            func.hour(DropLog.time)).all()
        else:
            pop_hours = DBSession.query(
                    func.hour(DropLog.time), func.count("*")
                    ).filter(DropLog.username == username
                    ).group_by(func.hour(DropLog.time)
                    ).order_by(func.hour(DropLog.time)).all()

    return [hour[1] for hour in pop_hours]

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


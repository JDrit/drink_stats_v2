from .models import DBSession, DropLog, DrinkItem, MoneyLog
from sqlalchemy import func
from datetime import datetime, timedelta

def top_spenders(limit = 10, start_date = None, end_date = None):
    if start_date and end_date and start_date <= end_date:
        return DBSession.query(MoneyLog.username, func.sum(func.abs(MoneyLog.amount))
                ).filter(MoneyLog.reason == 'drop', MoneyLog.time >= start_date,
                        MoneyLog.time <= end_date
                ).group_by(MoneyLog.username
                ).order_by('sum_1 desc').limit(limit).all()
    else:
        return DBSession.query(MoneyLog.username, func.sum(func.abs(MoneyLog.amount))
                ).filter(MoneyLog.reason == 'drop',
                ).group_by(MoneyLog.username
                ).order_by('sum_1 desc').limit(limit).all()
import time
def money_spent(username):
    return DBSession.query(func.sum(func.abs(MoneyLog.amount))).filter(MoneyLog.username == username, MoneyLog.reason == 'drop').first()[0]



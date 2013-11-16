from .models import DBSession, DropLog, DrinkItem, MoneyLog
from sqlalchemy import func
from datetime import datetime, timedelta

def top_spenders(limit = 10):
    return DBSession.query(MoneyLog.username, func.sum(func.abs(MoneyLog.amount))
            ).filter(MoneyLog.reason == 'drop'
            ).group_by(MoneyLog.username
            ).order_by('sum_1 desc').limit(limit).all()


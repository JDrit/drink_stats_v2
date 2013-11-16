from .models import DBSession, Machine
from sqlalchemy import func
from datetime import datetime, timedelta

def get_machine_name(machine_id):
    return DBSession.query(Machine.display_name).filter(Machine.machine_id == machine_id).first()[0]



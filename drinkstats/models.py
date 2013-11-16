from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    DateTime,
    Numeric,
    Enum
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class DropLog(Base):
    __tablename__ = 'drop_log'
    drop_log_id = Column(Integer, primary_key = True,
            autoincrement = True)
    machine_id = Column(Integer)
    slot = Column(String(length = 50))
    username = Column(String(length = 50))
    time = Column(DateTime)
    status = Column(String(length = 50))
    item_id = Column(Integer)
    current_item_price = Column(Integer)

    def __init__(self, machine_id, slot, username, time, status,
            item_id, current_item_price):
        self.machine_id = machine_id
        self.slot = slot
        self.username = username
        self.time = time
        self.status = status
        self.item_id = item_id
        self.current_item_price = current_item_price

class DrinkItem(Base):
    __tablename__ = 'drink_items'
    item_id = Column(Integer, primary_key = True, autoincrement = True)
    item_name = Column(String(length = 255))
    item_price = Column(Numeric)
    date_added = Column(DateTime)
    state = Column(Enum('active', 'inactive'))

class MoneyLog(Base):
    __tablename__ = 'money_log'
    money_log_id = Column(Integer, primary_key = True,
            autoincrement = True)
    time = Column(DateTime)
    username = Column(String(length = 255))
    admin = Column(String(length = 255))
    amount = Column(Integer)
    direction = Column(Enum('out', 'in'))
    reason = Column(String(length = 255))

class Machine(Base):
    __tablename__ = 'machines'
    machine_id = Column(Integer, primary_key = True,
            autoincrement = True)
    name = Column(String(length = 50))
    display_name = Column(String(length = 100))


from peewee import CharField
from peewee import DateTimeField
from peewee import Model
from peewee import SqliteDatabase
from datetime import datetime

from ..utils import get_database

# db = get_database('user_manager')
db = SqliteDatabase('database.db')

class User(Model):
    username = CharField(max_length=32,primary_key=True)
    password = CharField(max_length=96)

    class Meta:
        database = db

class PendingRegistration(Model):
    username = CharField(max_length=32)
    password = CharField(max_length=8)

    class Meta:
        database = db

class Consumer(Model):
    username = CharField(max_length=32,primary_key=True)
    email = CharField(max_length=32)
    password = CharField(max_length=48)
    class Meta:
        database = db


class ConsumerRegistration(Model):
    registration_id = CharField(max_length=48)
    registrer = CharField(max_length=32)
    username = CharField(max_length=32)
    password = CharField(max_length=32)
    email = CharField(max_length=32)
    class Meta:
        database = db


class Session(Model):
    session_id = CharField(max_length=96,primary_key=True)
    username = CharField(max_length=32)
    address = CharField(max_length=32)
    start_time = DateTimeField(default=datetime.now)

    class Meta:
        database = db


class PasswordResetRequest(Model):
    username = CharField(max_length=32)
    secret = CharField(max_length=48)


class ConsumerSession(Session):
    pass


class UserSession(Session):
    pass
db.connect()

db.create_tables([
    Consumer,
    ConsumerRegistration,
    ConsumerSession,
    User,
    UserSession
    ],
    safe=True 
    )
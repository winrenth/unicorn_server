from peewee import *

db = SqliteDatabase('unicorn.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField()
    email = CharField()
    password = CharField()
    updated_on = DateTimeField(null=True)
    created = DateTimeField(constraints=[SQL("DEFAULT (datetime('now'))")])

class Station(BaseModel):
    device_id = CharField()
    name = CharField()
    location = CharField()
    longitude = CharField(null=True)
    latitude = CharField(null=True)
    last_seen = DateTimeField(null=True)
    created = DateTimeField(constraints=[SQL("DEFAULT (datetime('now'))")])

class Measurement(BaseModel):
    station =  ForeignKeyField(Station)
    timestamp = IntegerField(null=True)
    temperature = DecimalField(null=True)
    humidity = DecimalField(null=True)
    pressure = DecimalField(null=True)
    CO2 = DecimalField(null=True)
    light = IntegerField(null=True)
    snow = IntegerField(null=True)
    rain = IntegerField(null=True)
    battery = IntegerField(null=True)

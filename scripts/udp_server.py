#!/usr/bin/env python

import socket
import struct
import ctypes
import sys
import datetime
import json
import time
from peewee import *
from unicorn_sever.models import Station, Measurement, db
from unicorn_sever.structs import UnicornProto

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

# make sure DB is inited
db.create_tables([User, Station, Measurement], safe=True)

# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#now keep talking with the client
while 1:
    # receive data from client (data, addr)
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]
     
    if not data: 
        break
     
    measured = process_data(data)

    # send back the reply
    reply = get_reply(measured)
    s.sendto(reply)

s.close()


def process_data(data):
    # first decouple binary data
    barr = bytearray(data)
    proto = UnicornProto.from_buffer(barr)
    print proto.device
    for field in proto._fields_:
        print field[0], getattr(proto, field[0])   
    
    #get device
    station, _ = Station.get_or_create(
        device_id=proto.device,
    )

    # store parsed data into DB
    measured = Measurement.create(
        station=station,
        timestamp = proto.timestamp,
        temperature = proto.temperature,
        humidity = proto.humidity,
        pressure = proto.pressure,
        CO2 = proto.CO2,
        light = proto.light,
        snow = proto.snow_intensity,
        rain = proto.rain_intensity,
        battery = proto.battery,
    )

    return measured
    

def get_reply(measured):
    # get last ts from DB
    last = Measurement.select().where(Measurement.station == measured.station, Measurement.timestamp < measured.timestamp).order_by(Measurement.timestamp.desc()).first()
    ts = int(time.time())
    if last:
        ts = last.timestamp
    return ctypes.c_ulong(ts), addr)

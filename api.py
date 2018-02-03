import falcon
from falcon_cors import CORS
import sys, os
import datetime
import json
import time
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from models import Station, Measurement, db
import logging

# make sure DB is inited
db.create_tables([Station, Measurement], safe=True)





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
    

class RequireJSON(object):

    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
                href='http://docs.examples.com/api/json')

        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                    href='http://docs.examples.com/api/json')


class JSONTranslator(object):
    # NOTE: Starting with Falcon 1.3, you can simply
    # use req.media and resp.media for this instead.

    def process_request(self, req, resp):
        # req.stream corresponds to the WSGI wsgi.input environ variable,
        # and allows you to read bytes from the request body.
        #
        # See also: PEP 3333
        if req.content_length in (None, 0):
            # Nothing to do
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

        try:
            req.context['doc'] = json.loads(body.decode('utf-8'))

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

    def process_response(self, req, resp, resource):
        if 'result' not in resp.context:
            return

        resp.body = json.dumps(resp.context['result'], indent=4, sort_keys=True, default=str)

def max_body(limit):

    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = ('The size of the request is too large. The body must not '
                   'exceed ' + str(limit) + ' bytes in length.')

            raise falcon.HTTPRequestEntityTooLarge(
                'Request body is too large', msg)

    return hook


class StationsResource(object):

    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp, name=None):
        try:
            if not name:
                result = list(Station.select().dicts())
            else:
                result = model_to_dict(Station.get(name=name))
        except Exception as ex:
            self.logger.error(ex)
            print ex
            description = ('Aliens have attacked our base! We will '
                           'be back as soon as we fight them off. '
                           'We appreciate your patience.')

            raise falcon.HTTPServiceUnavailable(
                'Service Outage',
                description,
                30)

        resp.context['result'] = result
        resp.status = falcon.HTTP_200

    @falcon.before(max_body(64 * 1024))
    def on_post(self, req, resp, user_id):
        try:
            doc = req.context['doc']
        except KeyError:
            raise falcon.HTTPBadRequest(
                'Missing thing',
                'A thing must be submitted in the request body.')

        proper_thing = self.db.add_thing(doc)

        resp.status = falcon.HTTP_201
        resp.location = '/%s/things/%s' % (user_id, proper_thing['id'])


class MeasurementResource(object):

    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_get(self, req, resp, name=None):
        try:
            if name:
                result = list(Measurement.select(
                    Measurement.timestamp,
                    Measurement.temperature,
                    Measurement.pressure,
                    Measurement.humidity,
                    Measurement.light,
                    Measurement.CO2,
                    Measurement.rain,
                    Measurement.snow,
                    Measurement.battery,
                    Station.name,
                    Station.id,
                ).join(Station).where(Station.name == name).order_by(
                    Measurement.timestamp.asc()
                ).limit(100).dicts())
            else:
                result = list(Measurement.select(
                    Measurement.timestamp,
                    Measurement.temperature,
                    Measurement.pressure,
                    Measurement.humidity,
                    Measurement.light,
                    Measurement.CO2,
                    Measurement.rain,
                    Measurement.snow,
                    Measurement.battery,
                    Station.name,
                    Station.id,
                ).join(Station).order_by(Measurement.timestamp.asc()).limit(200).dicts())
        except Exception as ex:
            self.logger.error(ex)
            print ex
            description = ('Aliens have attacked our base! We will '
                           'be back as soon as we fight them off. '
                           'We appreciate your patience.')

            raise falcon.HTTPServiceUnavailable(
                'Service Outage',
                description,
                30)

        resp.context['result'] = result
        resp.status = falcon.HTTP_200

    @falcon.before(max_body(64 * 1024))
    def on_post(self, req, resp, user_id):
        try:
            doc = req.context['doc']
        except KeyError:
            raise falcon.HTTPBadRequest(
                'Missing thing',
                'A thing must be submitted in the request body.')

        proper_thing = self.db.add_thing(doc)

        resp.status = falcon.HTTP_201
        resp.location = '/%s/things/%s' % (user_id, proper_thing['id'])


cors = CORS(allow_origins_list=['http://localhost:3000', 'localhost:3000', 'http://localhost:8000', 'localhost:8000', ], allow_all_methods=True, allow_all_headers=True)

app = falcon.API(middleware=[
    cors.middleware,
    RequireJSON(),
    JSONTranslator(),
])

stations = StationsResource(db)
measurements = MeasurementResource(db)
app.add_route('/api/stations', stations)
app.add_route('/api/stations/{name}', stations)
app.add_route('/api/data', measurements)
app.add_route('/api/data/{name}', measurements)



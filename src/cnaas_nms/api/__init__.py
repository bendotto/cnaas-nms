#!/usr/bin/env python3

from flask import Flask, request
from flask_restful import Resource, Api

import yaml
from ast import literal_eval
from cnaas_nms.cmdb.device import Device
from cnaas_nms.cmdb.session import session_scope

app = Flask(__name__)
api = Api(app)

def build_filter(f_class, query):
    args = request.args
    print(args)
    if not 'filter' in args:
        return query
    split = args['filter'].split(',')
    if not len(split) == 2:
        # invalid
        return query
    attribute, value = split
    if not attribute in f_class.__table__._columns.keys():
        # invalid
        return query
    kwargs = {attribute: value}
    return query.filter_by(**kwargs)

class DeviceByIdApi(Resource):
    def get(self, device_id):
        result = []
        with session_scope() as session:
            instance = session.query(Device).filter(Device.id == device_id).first()
            if instance:
                result.append(instance.as_dict())
            else:
                return [], 404
        return result

class DevicesApi(Resource):
    def get(self):
        result = []
        filter_exp = None
        with session_scope() as session:
            query = session.query(Device)
            query = build_filter(Device, query)
            for instance in query:
                result.append(instance.as_dict())
        return result


api.add_resource(DeviceByIdApi, '/api/v1.0/device/<int:device_id>')
api.add_resource(DevicesApi, '/api/v1.0/device')

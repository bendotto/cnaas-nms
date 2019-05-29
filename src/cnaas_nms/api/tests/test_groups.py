import pprint
import shutil
import yaml
import pkg_resources
import os

import json
import unittest

from flask import request
from flask_restful import Resource

from cnaas_nms.api import app
from cnaas_nms.db.session import sqla_session, sqla_execute
from cnaas_nms.db.groups import Groups, DeviceGroups
from cnaas_nms.db.device import Device


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    def test_1_add_new_group(self):
        data = {
            'name': 'group0',
            'description': 'random description',
        }
        result = self.client.post('/api/v1.0/groups', json=data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json['status'], 'success')

    def test_2_get_group(self):
        with sqla_session() as session:
            instance: Groups = session.query(Groups).filter(Groups.name ==
                                                            'group0').one_or_none()
            self.assertNotEqual(instance, None)

    def test_3_modify_group(self):
        data = {'description': 'new description'}
        with sqla_session() as session:
            instance: Groups = session.query(Groups).filter(Groups.name ==
                                                            'group0').one_or_none()
            self.assertNotEqual(instance, None)
            group_id = instance.as_dict()['id']
        result = self.client.put('/api/v1.0/groups/group0', json=data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json['status'], 'success')

    def test_4_add_device(self):
        device_data = {
            "hostname": "groupdevice",
            "site_id": 1,
            "description": '',
            "management_ip": "10.1.2.3",
            "dhcp_ip": "11.1.2.3",
            "serial": '',
            "ztp_mac": "0800275C091F",
            "platform": "eos",
            "vendor": '',
            "model": '',
            "os_version": '',
            "state": "MANAGED",
            "device_type": "ACCESS",
        }
        result = self.client.post('/api/v1.0/device', json=device_data)
        self.assertEqual(result.status_code, 200)

    def test_5_add_device_to_group(self):
        device_id = 0
        result = self.client.get('/api/v1.0/device')
        json_data = json.loads(result.data.decode())
        for _ in json_data['data']['devices']:
            if _['hostname'] != 'groupdevice':
                continue
            device_id = _['id']
        self.assertIsNot(device_id, 0)
        data = {'id': device_id}
        result = self.client.post('/api/v1.0/groups/group0/devices', json=data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json['status'], 'success')

    def test_6_delete_device_from_group(self):
        device_id = 0
        result = self.client.get('/api/v1.0/device')
        json_data = json.loads(result.data.decode())
        json_data = json.loads(result.data.decode())
        for _ in json_data['data']['devices']:
            if _['hostname'] != 'groupdevice':
                continue
            device_id = _['id']
        self.assertIsNot(device_id, 0)
        result = self.client.delete(f'/api/v1.0/groups/group0/devices/{ device_id }')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json['status'], 'success')

    def test_8_delete_group(self):
        result = self.client.delete('/api/v1.0/groups/group0')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json['status'], 'success')

    def test_9_delete_device(self):
        device_id = 0
        result = self.client.get('/api/v1.0/device')
        json_data = json.loads(result.data.decode())
        for _ in json_data['data']['devices']:
            if _['hostname'] != 'groupdevice':
                continue
            device_id = _['id']
        self.assertIsNot(device_id, 0)
        result = self.client.delete(f'/api/v1.0/device/{ device_id }')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json['status'], 'success')


if __name__ == '__main__':
    unittest.main()
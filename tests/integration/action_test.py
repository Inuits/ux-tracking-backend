from flask import json
from rest_framework import status

from tests.integration_case import IntegrationCase


class ActionTest(IntegrationCase):

    def testGetActions(self):
        resp = self.client.get('/action', headers=self.getAuthHeader())

        assert status.is_success(resp.status_code)

    def testPostActions(self):
        resp = self.client.post('/action', headers=self.getAuthHeader(), json={'actions': json.dumps([
            {
                'client': 'hakka',
                'method': 'GET',
                'path': '/path/to/action/place',
                'position': '12,21',
                'session': 'admin',
                'type': 'REQ',
                'value': 'testvalue'
            }
        ])
        })

        assert status.is_success(resp.status_code)

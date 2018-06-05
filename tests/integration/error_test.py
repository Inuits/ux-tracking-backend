from rest_framework import status

from tests.integration_case import IntegrationCase


class ErrorTest(IntegrationCase):

    # def testGetErrorsWithoutAuth(self):
    #     from flask_jwt_extended.exceptions import NoAuthorizationError
    #
    #     with self.assertRaises(NoAuthorizationError):
    #         self.client.get('/error')

    def testGetErrorsEndpoint(self):
        resp = self.client.get('/error', headers=self.getAuthHeader())

        assert status.is_success(resp.status_code)

    def testPostError(self):
        resp = self.client.post('/error', headers=self.getAuthHeader(), json={
            'client': 'hakka',
            'session': 'info@hakka.eu',
            'error': 'this is an error',
            'source': '/source.ts',
            'position': '12,34',
            'stack': 'stacktracee',
            'actions': {},
            'timestamp': 1123454656
        })

        assert status.is_success(resp.status_code)
        assert resp.status_code is status.HTTP_201_CREATED


    def testPostErrorWithActions(self):
        resp = self.client.post('/error', headers=self.getAuthHeader(), json={
            'client': 'hakka',
            'session': 'info@hakka.eu',
            'error': 'this is a new error',
            'source': '/source.ts',
            'position': '12,34',
            'stack': 'stacktracee',
            'actions': '[{ "client": "hakka", "method": "GET", "path": "/pos.html", "position": "122341,23424", '
                       '"session": "info@hakka.eu", "type": "REQ", "value": "lol" }]',
            'timestamp': 987654321
        })

        assert status.is_success(resp.status_code)
        assert resp.status_code is status.HTTP_201_CREATED


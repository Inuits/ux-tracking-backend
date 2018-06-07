import unittest

from app.app import app


class IntegrationCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        self.client.preserve_context = True
        self.loadToken()

    def tearDown(self):
        self.client = None

    def loadToken(self):
        resp =  self.client.post('/auth', data={'name': 'sportoffice', 'key': 'sportoase'})
        self.token = resp.get_json()['access_token']

    def getAuthHeader(self):
        return {'Authorization': 'Bearer ' + self.token}
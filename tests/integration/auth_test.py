from tests.integration_case import IntegrationCase


class AuthTest(IntegrationCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testGetOnAuth(self):
        resp = self.client.get('/auth')
        self.assertEqual(405, resp.status_code)  # 405: Method Not Allowed

    def testCredentials(self):
        resp = self.client.post('/auth', data=dict(name='matty', key='debie'))

        self.assertEqual(200, resp.status_code)

    def testWrongCredentials(self):
        resp = self.client.post('/auth', data=dict(
            name='wrong',
            key='creds'
        ))
        self.assertEqual(401, resp.status_code)

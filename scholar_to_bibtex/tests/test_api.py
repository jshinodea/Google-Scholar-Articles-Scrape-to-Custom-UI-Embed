import unittest
import json
from src.app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')

    def test_missing_url(self):
        response = self.app.post('/convert',
                               data=json.dumps({}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400) 
import falcon
from falcon import testing
import unittest
import webapi
import metadata
from mongoengine import connect

class TestIntAPI(testing.TestCase):
    def setUp(self):
        super().setUp()
        
        connect('metaddata', host='mongomock://localhost', alias='metadata')
        config = {
            "auth_key_file": "config/auth.key",
            "celery_config": "config/celery_config.json",
            "metadata_config": {},
        }
        self.app = webapi.main(config)

class TestDatasets(TestIntAPI):
    def test_configure_api_v1(self):
        body= {'ids': []}
        result = self.simulate_get('/api/v1/datasets')
        self.assertEqual(result.json, body)

    def test_configure_api_v2(self):
        body= {'error': 'Dataset metadata doesnt exist'}
        result = self.simulate_get('/api/v1/dataset/{id}')
        self.assertEqual(result.json, body)

class TestArchitecture(TestIntAPI):
    def test_configure_api_v3(self):
        body= {'ids': []}
        result = self.simulate_get('/api/v1/architectures')
        self.assertEqual(result.json, body)

    def test_configure_api_v4(self):
        body= {'error': 'Architecture does not exist'}
        result = self.simulate_get('/api/v1/architecute/{id}')
        self.assertEqual(result.status, falcon.HTTP_404)

import falcon
from falcon import testing
import unittest
import webapi
import metadata
from mongoengine import connect

class Testdatasets(testing.TestCase):
    def setUp(self):
        super(Testdatasets, self).setUp()
        
        connect('metaddata', host='mongomock://localhost', alias='metadata')
        self.app = webapi.main()

class TestDatasets(Testdatasets):
    def test_configure_api_v1(self):
        body= {'ids': []}
        result = self.simulate_get('/api/v1/datasets')
        self.assertEqual(result.json, body)

    def test_configure_api_v2(self):
        body= {'error': 'Dataset metadata doesnt exist'}
        result = self.simulate_get('/api/v1/dataset/{id}')
        self.assertEqual(result.json, body)

class TestArchitecture(Testdatasets):
    def test_configure_api_v3(self):
        body= {'ids': []}
        result = self.simulate_get('/api/v1/architectures')
        self.assertEqual(result.json, body)

    def test_configure_api_v4(self):
        body= {'error': 'Architecture does not exist'}
        result = self.simulate_get('/api/v1/architecute/{id}')
        self.assertEqual(result.status, falcon.HTTP_404)

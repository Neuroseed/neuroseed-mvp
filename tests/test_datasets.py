import falcon
from falcon import testing
import unittest
import webapi
import uuid
import metadata
import jwt
from mongoengine import connect


class TestIntAPI(testing.TestCase):
    def create_token(self, user_id):
        payload = {
            'user_id': user_id
        }
        token = jwt.encode(payload, self.SECRET_KEY, algorithm='HS256').decode('utf-8')
        return token
        
    def get_auth_headers(self, token):
        headers = {'Authorization': 'Bearer {token}'.format(token=token)}
        return headers

    def setUp(self):
        super().setUp()
        connect('metaddata', host='mongomock://localhost', alias='metadata')
        config = {
            "auth_key_file": "config/auth.key",
            "celery_config": "config/celery_config.json",
            "metadata_config": {},
        }
        self.SECRET_KEY = open(config["auth_key_file"]).read()
        self.app = webapi.main(config)


class TestDatasets(TestIntAPI):
    def setUp(self):
        super().setUp()
        document = {
            'is_public': False
            }
        dataset_meta = metadata.DatasetMetadata(**document)
        dataset_meta.id = str(uuid.uuid4())
        dataset_meta.url = dataset_meta.id
        dataset_meta.base.owner = "user_id"
        dataset_meta.save()
        self.dataset_meta = dataset_meta

    def tearDown(self):
        metadata.DatasetMetadata.objects.all().delete()
    
    def test_get_datasets(self):
        body= {'ids': [self.dataset_meta.id]}
        token = self.create_token("user_id")
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/datasets', headers=headers)
        self.assertEqual(result.json, body)
    

    def test_get_dataset_id(self):
        body= {'error': 'Dataset metadata doesnt exist'}
        token = self.create_token("user_id")
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/dataset/{id}'.format(id=self.dataset_meta.id), headers=headers)
        self.assertEqual(result.status, falcon.HTTP_200)


'''
class TestArchitecture(TestIntAPI):
    def setUp(self):
        super().setUp()
    def test_configure_api_v3(self):
        body= {'ids': []}
        result = self.simulate_get('/api/v1/architectures')
        self.assertEqual(result.json, body)

    def test_configure_api_v4(self):
        body= {'error': 'Architecture does not exist'}
        result = self.simulate_get('/api/v1/architecute/{id}')
        self.assertEqual(result.status, falcon.HTTP_404)

'''

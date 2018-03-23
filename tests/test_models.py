import falcon
from falcon import testing
import webapi
import uuid
import metadata
import jwt
from mongoengine import connect


class TestInitAPI(testing.TestCase):
    def create_token(self, user_id):
        payload = {
            'user_id': user_id
        }
        token = jwt.encode(payload, self.SECRET_KEY, algorithm='HS256').decode('utf-8')
        return token
        
    def get_auth_headers(self, token):
        return {
            'Authorization': 'Bearer {token}'.format(token=token)
        }

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


class TestModels(TestInitAPI):
    def tearDown(self):
        metadata.DatasetMetadata.objects.all().delete()

    def create_arch_metadata(self, is_public, owner):
        architecture = metadata.ArchitectureMetadata()
        architecture.id = str(uuid.uuid4())
        architecture.owner = owner
        architecture.title = 'title'
        architecture.architecture = {'layers': []}
        architecture.save()

        return architecture

    def create_model_metadata(self, is_public, owner):
        model = metadata.ModelMetadata(is_public=is_public)
        model.id = str(uuid.uuid4())
        model.url = model.id
        model.base.owner = owner
        model.base.title = 'title'
        model.base.architecture = self.create_arch_metadata(True, owner)
        model.save()

        return model
    
    def test_schema_no_auth(self):
        self.create_model_metadata(True, 'u1')

        result = self.simulate_get('/api/v1/models')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate schema
        self.assertEqual(list(result.json.keys()), ['ids'])

    def test_schema_auth(self):
        self.create_model_metadata(True, 'u1')

        token = self.create_token("u1")
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/models', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate schema
        self.assertEqual(list(result.json.keys()), ['ids'])

    def test_many_public_models_no_auth(self):
        user_id = 'u1'
        models = [self.create_model_metadata(True, user_id).id for _ in range(3)]

        result = self.simulate_get('/api/v1/models')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate schema
        for id in models:
            self.assertTrue(id in result.json['ids'])

    def test_many_private_models_no_auth(self):
        user_id = 'u1'
        models = [self.create_model_metadata(False, user_id).id for _ in range(3)]

        result = self.simulate_get('/api/v1/models')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate schema
        for id in models:
            self.assertFalse(id in result.json['ids'])

    def test_many_private_models_auth(self):
        user_id = 'u1'
        another_user_id = 'u2'

        my_models = [self.create_model_metadata(False, user_id).id for _ in range(3)]
        not_my_models = [self.create_model_metadata(False, another_user_id).id for _ in range(3)]

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/models', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        for id in my_models:
            self.assertTrue(id in result.json['ids'])

        for id in not_my_models:
            self.assertFalse(id in result.json['ids'])

    def test_get_dataset(self):
        result = self.simulate_get('/api/v1/model')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_404)

    def test_create_model_no_auth(self):
        json = {}
        result = self.simulate_post('/api/v1/model', json=json)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_401)

    def test_create_model_auth_arch_does_not_exist(self):
        json = {
            'title': 'title',
            'architecture': 'some-architecture-id'
        }
        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_post('/api/v1/model', json=json, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_404)

    def test_create_model_auth_arch_another_user(self):
        a1 = self.create_arch_metadata(False, 'u2')
        json = {
            'title': 'title',
            'architecture': a1.id
        }
        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_post('/api/v1/model', json=json, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_404)

    def test_create_model_auth(self):
        a1 = self.create_arch_metadata(True, 'u1')

        json = {
            'title': 'title',
            'architecture': a1.id
        }
        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_post('/api/v1/model', json=json, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

    def test_update_model(self):
        m1 = self.create_model_metadata(True, 'u1')

        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        url = '/api/v1/model/{id}'.format(id=m1.id)
        result = self.simulate_post(url, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_400)

    def test_get_one_dataset_no_auth(self):
        m1 = self.create_model_metadata(True, 'u1')

        url = '/api/v1/model/{id}'.format(id=m1.id)
        result = self.simulate_get(url)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate id
        self.assertEqual(result.json['id'], m1.id)

    def test_get_one_private_dataset_no_auth(self):
        m1 = self.create_model_metadata(False, 'u1')

        url = '/api/v1/model/{id}'.format(id=m1.id)
        result = self.simulate_get(url)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_404)

    def test_get_one_dataset_auth(self):
        m1 = self.create_model_metadata(False, 'u1')

        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        url = '/api/v1/model/{id}'.format(id=m1.id)
        result = self.simulate_get(url, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate id
        self.assertEqual(result.json['id'], m1.id)

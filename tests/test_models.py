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

    def tearDown(self):
        metadata.DatasetMetadata.objects.all().delete()
        metadata.ArchitectureMetadata.objects.all().delete()
        metadata.ModelMetadata.objects.all().delete()

    def create_dataset_metadata(self, is_public, owner):
        dataset = metadata.DatasetMetadata()
        dataset.is_public = is_public
        dataset.base.owner = owner
        dataset.id = str(uuid.uuid4())
        dataset.url = dataset.id
        dataset.base.title = 'title'
        dataset.save()

        return dataset

    def create_arch_metadata(self, is_public, owner):
        architecture = metadata.ArchitectureMetadata()
        architecture.id = str(uuid.uuid4())
        architecture.is_public = is_public
        architecture.owner = owner
        architecture.title = 'title'
        architecture.architecture = {'layers': []}
        architecture.save()

        return architecture

    def create_model_metadata(self, is_public, owner):
        model = metadata.ModelMetadata()
        model.id = str(uuid.uuid4())
        model.url = model.id
        model.is_public = is_public
        model.base.owner = owner
        model.base.title = 'title'
        model.base.architecture = self.create_arch_metadata(is_public, owner)
        model.base.dataset = self.create_dataset_metadata(is_public, owner)
        model.save()

        return model


class TestModels(TestInitAPI):
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

    def test_get_model(self):
        result = self.simulate_get('/api/v1/model')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_404)

    def test_create_model_no_auth(self):
        json = {}
        result = self.simulate_post('/api/v1/model', json=json)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_401)


class TestModel(TestInitAPI):
    def test_create_model_auth_arch_does_not_exist(self):
        d1 = self.create_dataset_metadata(True, 'u1')
        json = {
            'title': 'title',
            'architecture': 'some-architecture-id',
            'dataset': d1.id
        }
        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_post('/api/v1/model', json=json, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_404)

    def test_create_model_auth_arch_another_user(self):
        a1 = self.create_arch_metadata(False, 'u2')
        d1 = self.create_dataset_metadata(True, 'u1')
        json = {
            'title': 'title',
            'architecture': a1.id,
            'dataset': d1.id
        }
        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_post('/api/v1/model', json=json, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_404)

    def test_create_model_auth(self):
        a1 = self.create_arch_metadata(True, 'u1')
        d1 = self.create_dataset_metadata(True, 'u1')

        json = {
            'title': 'title',
            'architecture': a1.id,
            'dataset': d1.id
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

    def test_get_one_model_no_auth(self):
        m1 = self.create_model_metadata(True, 'u1')

        url = '/api/v1/model/{id}'.format(id=m1.id)
        result = self.simulate_get(url)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate id
        self.assertEqual(result.json['id'], m1.id)

    def test_get_one_private_model_no_auth(self):
        m1 = self.create_model_metadata(False, 'u1')

        url = '/api/v1/model/{id}'.format(id=m1.id)
        result = self.simulate_get(url)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_404)

    def test_get_one_model_auth(self):
        m1 = self.create_model_metadata(False, 'u1')

        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        url = '/api/v1/model/{id}'.format(id=m1.id)
        result = self.simulate_get(url, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate id
        self.assertEqual(result.json['id'], m1.id)

    def test_get_other_public_model_with_auth(self):
        user_1 = 'u1'
        user_2 = 'u2'

        not_my_public_model = self.create_model_metadata(True, user_2)

        token = self.create_token(user_1)
        headers = self.get_auth_headers(token)
        url = '/api/v1/model/{id}'.format(id=not_my_public_model.id)
        result = self.simulate_get(url, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertTrue(not_my_public_model.id, result.json['id'])


class TestModelsFull(TestInitAPI):
    def test_get_empty(self):
        result = self.simulate_get('/api/v1/models/full')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

    def test_get_one(self):
        a1 = self.create_model_metadata(True, 'u1')

        result = self.simulate_get('/api/v1/models/full')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        models = result.json['models']
        self.assertEqual(len(models), 1)

        self.assertEqual(models[0]['id'], a1.id)

    def test_get_many_no_auth(self):
        number = 5
        [self.create_model_metadata(True, 'u1') for _ in range(number)]

        result = self.simulate_get('/api/v1/models/full')

        # validate codes
        self.assertEqual(result.status, falcon.HTTP_200)

        models = result.json['models']
        self.assertEqual(len(models), number)

    def test_get_many_auth(self):
        number = 5
        [self.create_model_metadata(False, 'u1') for _ in range(number)]
        [self.create_model_metadata(False, 'u2') for _ in range(number)]

        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/models/full', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        models = result.json['models']
        self.assertEqual(len(models), number)

    def test_query_slice_on_border(self):
        number = 20
        [self.create_model_metadata(True, 'u1') for _ in range(number)]

        from_ = 10
        n = 20
        query_string = 'from={f}&number={n}'.format(f=from_, n=n)
        result = self.simulate_get('/api/v1/models/full', query_string=query_string)

        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertEqual(len(result.json['models']), number - from_)

    def test_query_invalid_slice(self):
        number = 5
        [self.create_model_metadata(True, 'u1') for _ in range(number)]

        query_string = 'from=-2&number=3'
        result = self.simulate_get('/api/v1/models/full', query_string=query_string)
        self.assertEqual(result.status, falcon.HTTP_400)

        query_string = 'from=1&number=-3'
        result = self.simulate_get('/api/v1/models/full', query_string=query_string)
        self.assertEqual(result.status, falcon.HTTP_400)


class TestModelsNumber(TestInitAPI):
    def test_get_number_of_empty(self):
        result = self.simulate_get('/api/v1/models/number')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        self.assertEqual(result.json, 0)

    def test_get_number_one(self):
        m1 = self.create_model_metadata(True, 'u1')

        result = self.simulate_get('/api/v1/models/number')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        self.assertEqual(result.json, 1)

    def test_get_number_many(self):
        number = 15
        models = [self.create_model_metadata(True, 'u1') for _ in range(number)]

        result = self.simulate_get('/api/v1/models/number')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        self.assertEqual(result.json, number)

    def test_get_number_many_auth(self):
        number = 5
        models = [self.create_model_metadata(False, 'u1') for _ in range(number)]
        models = [self.create_model_metadata(True, 'u1') for _ in range(number)]
        models = [self.create_model_metadata(False, 'u2') for _ in range(number)]
        models = [self.create_model_metadata(True, 'u2') for _ in range(number)]

        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/models/number', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        self.assertEqual(result.json, 3 * number)

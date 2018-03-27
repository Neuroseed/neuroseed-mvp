import falcon
from falcon import testing
import unittest
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

    def tearDown(self):
        metadata.DatasetMetadata.objects.all().delete()

    def create_dataset_metadata(self, is_public, owner):
        dataset = metadata.DatasetMetadata()
        dataset.is_public = is_public
        dataset.base.owner = owner
        dataset.id = str(uuid.uuid4())
        dataset.url = dataset.id
        dataset.base.title = 'title'
        dataset.save()

        return dataset


class TestDatasets(TestInitAPI):
    def test_get_many_datasets_no_auth(self):
        user_id = 'user1'
        datasets_no_auth = [self.create_dataset_metadata(True, user_id).id for _ in range(3)]
        result = self.simulate_get('/api/v1/datasets')
        self.assertEqual(result.status, falcon.HTTP_200)
        for id in datasets_no_auth:
            self.assertTrue(id in result.json['ids'])

    def test_get_many_datasets_auth(self):
        user_id = 'user1'
        another_user_id = 'user2'
        my_datasets = [self.create_dataset_metadata(False, user_id).id for _ in range(3)]
        not_my_datasets = [self.create_dataset_metadata(False, another_user_id).id for _ in range(3)]
        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/datasets', headers=headers)
        self.assertEqual(result.status, falcon.HTTP_200)
        for id in my_datasets:
            self.assertTrue(id in result.json['ids'])
        for id in not_my_datasets:
            self.assertFalse(id in result.json['ids'])


class TestDataset(TestInitAPI):
    def test_get_dataset_id_no_auth(self):
        user_id = 'user1'
        no_auth_dataset = self.create_dataset_metadata(True, user_id)
        result = self.simulate_get('/api/v1/dataset/{id}'.format(id=no_auth_dataset.id))
        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertEqual(no_auth_dataset.id, result.json['id'])

    def test_get_dataset_id_auth(self):
        user_id = 'user1'
        another_user_id = 'user2'

        my_dataset = self.create_dataset_metadata(True, user_id)
        not_my_dataset = self.create_dataset_metadata(False, another_user_id)

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/dataset/{id}'.format(id=my_dataset.id), headers=headers)

        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertTrue(my_dataset.id, result.json['id'])

    def test_get_other_public_dataset_with_auth(self):
        user_1 = 'u1'
        user_2 = 'u2'

        not_my_public_dataset = self.create_dataset_metadata(True, user_2)

        token = self.create_token(user_1)
        headers = self.get_auth_headers(token)
        url = '/api/v1/dataset/{id}'.format(id=not_my_public_dataset.id)
        result = self.simulate_get(url, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertTrue(not_my_public_dataset.id, result.json['id'])

    def test_create_dataset_auth(self):
        user_id = 'user1'
        ds1 = self.create_dataset_metadata(True, user_id)
        json = {
            'title': 'title',
            'description': 'description'
        }
        url = '/api/v1/dataset/{id}'.format(id=ds1.id)
        result = self.simulate_post(url, json=json)
        self.assertEqual(result.status, falcon.HTTP_401)

    def test_get_dataset_does_not_exist(self):
        result = self.simulate_get('/api/v1/dataset/dataset-id')
        self.assertEqual(result.status, falcon.HTTP_404)


class TestDatasetssFull(TestInitAPI):
    def test_get_empty(self):
        result = self.simulate_get('/api/v1/datasets/full')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

    def test_get_one(self):
        d1 = self.create_dataset_metadata(True, 'u1')

        result = self.simulate_get('/api/v1/datasets/full')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        datasets = result.json['datasets']
        self.assertEqual(len(datasets), 1)

        self.assertEqual(datasets[0]['id'], d1.id)

    def test_get_many_no_auth(self):
        number = 5
        [self.create_dataset_metadata(True, 'u1') for _ in range(number)]

        result = self.simulate_get('/api/v1/datasets/full')

        # validate codes
        self.assertEqual(result.status, falcon.HTTP_200)

        datasets = result.json['datasets']
        self.assertEqual(len(datasets), number)

    def test_get_many_auth(self):
        number = 5
        [self.create_dataset_metadata(False, 'u1') for _ in range(number)]
        [self.create_dataset_metadata(False, 'u2') for _ in range(number)]

        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/datasets/full', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        datasets = result.json['datasets']
        self.assertEqual(len(datasets), number)

    def test_query_slice(self):
        number = 5
        [self.create_dataset_metadata(True, 'u1') for _ in range(number)]

        query_string = 'from=-2&number=3'
        result = self.simulate_get('/api/v1/datasets/full', query_string=query_string)
        self.assertEqual(result.status, falcon.HTTP_400)

        query_string = 'from=1&number=-3'
        result = self.simulate_get('/api/v1/datasets/full', query_string=query_string)
        self.assertEqual(result.status, falcon.HTTP_400)


class TestDatasetsNumber(TestInitAPI):
    def test_get_number_of_empty(self):
        result = self.simulate_get('/api/v1/datasets/number')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        self.assertEqual(result.json, 0)

    def test_get_number_one(self):
        d1 = self.create_dataset_metadata(True, 'u1')

        result = self.simulate_get('/api/v1/datasets/number')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        self.assertEqual(result.json, 1)

    def test_get_number_many(self):
        number = 15
        datasets = [self.create_dataset_metadata(True, 'u1') for _ in range(number)]

        result = self.simulate_get('/api/v1/datasets/number')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        self.assertEqual(result.json, number)

    def test_get_number_many_auth(self):
        number = 5
        datasets = [self.create_dataset_metadata(False, 'u1') for _ in range(number)]
        datasets = [self.create_dataset_metadata(True, 'u1') for _ in range(number)]
        datasets = [self.create_dataset_metadata(False, 'u2') for _ in range(number)]
        datasets = [self.create_dataset_metadata(True, 'u2') for _ in range(number)]

        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/datasets/number', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        self.assertEqual(result.json, 3 * number)

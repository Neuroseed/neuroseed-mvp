import uuid
import tempfile

import jwt
import falcon
from falcon import testing
from mongoengine import connect

import webapi
import metadata
import storage


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

        test_dir = tempfile.mkdtemp('test_home')
        storage.from_config({
            'home': test_dir
        })

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

    def test_get_dataset_does_not_exist(self):
        result = self.simulate_get('/api/v1/dataset/dataset-id')
        self.assertEqual(result.status, falcon.HTTP_404)


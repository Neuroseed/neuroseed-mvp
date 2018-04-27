import os
import uuid
import io
import tempfile

import jwt
import falcon
from falcon import testing
from mongoengine import connect
from requests_toolbelt.multipart import encoder
import h5py

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

    def upload(self, dataset_id, file_io, headers={}):
        form = encoder.MultipartEncoder({
            "file": ('dataset.hdf5', file_io, "text/plain")
        })

        headers.update({
            "Prefer": "respond-async",
            "Content-Type": form.content_type,
        })

        url = '/api/v1/dataset/{}'.format(dataset_id)
        resp = self.simulate_post(url, headers=headers, body=form.read())

        return resp

    def test_upload_dataset_no_auth(self):
        user_1 = 'u1'
        d1 = self.create_dataset_metadata(True, user_1)

        file_io = io.BytesIO(b'bytes')
        resp = self.upload(d1.id, file_io)

        self.assertEqual(resp.status, falcon.HTTP_401)

    def test_upload_dataset_not_hdf5(self):
        user_1 = 'u1'
        d1 = self.create_dataset_metadata(True, user_1)

        token = self.create_token(user_1)
        headers = self.get_auth_headers(token)

        file_io = io.BytesIO(b'bytes')
        resp = self.upload(d1.id, file_io, headers)

        self.assertEqual(resp.status, falcon.HTTP_415)

    def test_upload_dataset_hdf5_invalid_structure(self):
        user_1 = 'u1'
        d1 = self.create_dataset_metadata(True, user_1)

        token = self.create_token(user_1)
        headers = self.get_auth_headers(token)

        # create hdf5
        test_file_path = storage.get_tmp_path('test')
        with h5py.File(test_file_path, 'w') as f:
            _ = f.create_dataset('x', shape=(1,))

        with open(test_file_path, 'rb') as file_io:
            resp = self.upload(d1.id, file_io, headers)

        os.remove(test_file_path)

        self.assertEqual(resp.status, falcon.HTTP_415)

    def test_upload_dataset_hdf5_valid_structure(self):
        user_1 = 'u1'
        d1 = self.create_dataset_metadata(True, user_1)

        token = self.create_token(user_1)
        headers = self.get_auth_headers(token)

        # create hdf5
        test_file_path = storage.get_tmp_path('test')
        with h5py.File(test_file_path, 'w') as f:
            _ = f.create_dataset('x', shape=(1,))
            _ = f.create_dataset('y', shape=(1,))

        with open(test_file_path, 'rb') as file_io:
            resp = self.upload(d1.id, file_io, headers)

        os.remove(test_file_path)

        self.assertEqual(resp.status, falcon.HTTP_200)
        self.assertTrue('id' in resp.json.keys())

    def test_upload_dataset_hdf5_too_large(self):
        user_1 = 'u1'
        d1 = self.create_dataset_metadata(True, user_1)

        token = self.create_token(user_1)
        headers = self.get_auth_headers(token)
        headers.update({
            'Content-Length': str(10**20)
        })

        # create hdf5
        test_file_path = storage.get_tmp_path('test')
        with h5py.File(test_file_path, 'w') as f:
            _ = f.create_dataset('x', shape=(1,))
            _ = f.create_dataset('y', shape=(1,))

        with open(test_file_path, 'rb') as file_io:
            resp = self.upload(d1.id, file_io, headers)

        os.remove(test_file_path)

        self.assertEqual(resp.status, falcon.HTTP_413)


class TestDeleteDataset(TestInitAPI):
    def test_delete_dataset_no_auth(self):
        user_id = 'u1'
        d1 = self.create_dataset_metadata(True, user_id)

        url = '/api/v1/dataset/{id}'.format(id=d1.id)
        result = self.simulate_delete(url)

        self.assertEqual(result.status, falcon.HTTP_401)

    def test_delete_dataset(self):
        user_id = 'u1'
        d1 = self.create_dataset_metadata(True, user_id)

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        url = '/api/v1/dataset/{id}'.format(id=d1.id)
        result = self.simulate_delete(url, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_200)

    def delete_others_dataset(self):
        user_id = 'u1'
        other_user_id = 'u2'
        d1 = self.create_dataset_metadata(False, other_user_id)

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        url = '/api/v1/dataset/{id}'.format(id=d1.id)
        result = self.simulate_delete(url, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_404)

    def delete_not_exist_dataset(self):
        user_id = 'u1'
        dataset_id = 'dataset-id'
        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        url = '/api/v1/dataset/{id}'.format(id=dataset_id)
        result = self.simulate_delete(url, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_404)

    def test_delete_published_dataset(self):
        user_id = 'u1'
        d1 = self.create_dataset_metadata(True, user_id)

        d1.status = metadata.dataset.PUBLISHED
        d1.save()

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        url = '/api/v1/dataset/{id}'.format(id=d1.id)
        result = self.simulate_delete(url, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_409)


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
        number = 50
        [self.create_dataset_metadata(True, 'u1') for _ in range(number)]

        from_ = 10
        n = 20
        query_string = 'from={f}&number={n}'.format(f=from_, n=n)
        result = self.simulate_get('/api/v1/datasets/full', query_string=query_string)

        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertEqual(len(result.json['datasets']), n)

    def test_query_slice_on_border(self):
        number = 20
        [self.create_dataset_metadata(True, 'u1') for _ in range(number)]

        from_ = 10
        n = 20
        query_string = 'from={f}&number={n}'.format(f=from_, n=n)
        result = self.simulate_get('/api/v1/datasets/full', query_string=query_string)

        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertEqual(len(result.json['datasets']), number - from_)

    def test_query_invalid_slice(self):
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

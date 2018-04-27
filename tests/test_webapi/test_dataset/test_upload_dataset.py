import os
import io

import falcon
from requests_toolbelt.multipart import encoder
import h5py

import storage

from .test_dataset import TestInitAPI


class TestUploadDataset(TestInitAPI):
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

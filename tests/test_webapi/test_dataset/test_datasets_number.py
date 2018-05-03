import os
import uuid
import io
import falcon

from .test_dataset import TestInitAPI


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

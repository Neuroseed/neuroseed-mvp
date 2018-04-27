import falcon

import metadata

from .test_dataset import TestInitAPI


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

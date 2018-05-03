import falcon

from .test_dataset import TestInitAPI


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

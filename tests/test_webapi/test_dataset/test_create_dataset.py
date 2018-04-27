import falcon

from .test_dataset import TestInitAPI


class TestCreateDataset(TestInitAPI):
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

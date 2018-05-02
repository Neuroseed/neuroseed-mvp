import falcon

from .test_model import TestInitAPI


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

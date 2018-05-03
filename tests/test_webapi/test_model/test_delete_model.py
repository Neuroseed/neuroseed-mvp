import falcon

import metadata

from .test_model import TestInitAPI


class TestModel(TestInitAPI):
    def test_delete_model_no_auth(self):
        user = 'u1'
        m1 = self.create_model_metadata(True, user)

        url = '/api/v1/model/{id}'.format(id=m1.id)
        result = self.simulate_delete(url)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_401)

    def test_delete_model_auth(self):
        user = 'u1'
        m1 = self.create_model_metadata(True, user)

        token = self.create_token(user)
        headers = self.get_auth_headers(token)
        url = '/api/v1/model/{id}'.format(id=m1.id)
        result = self.simulate_delete(url, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

    def test_delete_others_model(self):
        user_id = 'u1'
        other_user_id = 'u2'
        m1 = self.create_model_metadata(False, other_user_id)

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        url = '/api/v1/model/{id}'.format(id=m1.id)
        result = self.simulate_delete(url, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_404)

    def test_delete_not_exist_model(self):
        user_id = 'u1'
        model_id = 'model-id'
        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        url = '/api/v1/model/{id}'.format(id=model_id)
        result = self.simulate_delete(url, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_404)

    def test_delete_published_model(self):
        user_id = 'u1'
        m1 = self.create_model_metadata(True, user_id)

        m1.status = metadata.model.PUBLISHED
        m1.save()

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        url = '/api/v1/model/{id}'.format(id=m1.id)
        result = self.simulate_delete(url, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_409)

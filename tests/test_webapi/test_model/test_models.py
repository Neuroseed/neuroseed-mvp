import falcon

from .test_model import TestInitAPI


class TestModels(TestInitAPI):
    def test_schema_no_auth(self):
        self.create_model_metadata(True, 'u1')

        result = self.simulate_get('/api/v1/models')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate schema
        self.assertEqual(list(result.json.keys()), ['ids'])

    def test_schema_auth(self):
        self.create_model_metadata(True, 'u1')

        token = self.create_token("u1")
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/models', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate schema
        self.assertEqual(list(result.json.keys()), ['ids'])

    def test_many_public_models_no_auth(self):
        user_id = 'u1'
        models = [self.create_model_metadata(True, user_id).id for _ in range(3)]

        result = self.simulate_get('/api/v1/models')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate schema
        for id in models:
            self.assertTrue(id in result.json['ids'])

    def test_many_private_models_no_auth(self):
        user_id = 'u1'
        models = [self.create_model_metadata(False, user_id).id for _ in range(3)]

        result = self.simulate_get('/api/v1/models')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate schema
        for id in models:
            self.assertFalse(id in result.json['ids'])

    def test_many_private_models_auth(self):
        user_id = 'u1'
        another_user_id = 'u2'

        my_models = [self.create_model_metadata(False, user_id).id for _ in range(3)]
        not_my_models = [self.create_model_metadata(False, another_user_id).id for _ in range(3)]

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/models', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        for id in my_models:
            self.assertTrue(id in result.json['ids'])

        for id in not_my_models:
            self.assertFalse(id in result.json['ids'])

    def test_get_model(self):
        result = self.simulate_get('/api/v1/model')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_404)

    def test_create_model_no_auth(self):
        json = {}
        result = self.simulate_post('/api/v1/model', json=json)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_401)

import falcon

from .test_architecture import TestInitAPI


class TestArchitectures(TestInitAPI):
    def test_schema_no_auth(self):
        self.create_arch_metadata(True, 'u1')

        result = self.simulate_get('/api/v1/architectures')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate schema
        self.assertEqual(list(result.json.keys()), ['ids'])

    def test_schema_auth(self):
        self.create_arch_metadata(True, 'u1')

        token = self.create_token("u1")
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/architectures', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate schema
        self.assertEqual(list(result.json.keys()), ['ids'])

    def test_many_public_architectures_no_auth(self):
        user_id = 'u1'
        models = [self.create_arch_metadata(True, user_id).id for _ in range(3)]

        result = self.simulate_get('/api/v1/architectures')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate schema
        for id in models:
            self.assertTrue(id in result.json['ids'])

    def test_many_private_architectures_no_auth(self):
        user_id = 'u1'
        architectures = [self.create_arch_metadata(False, user_id).id for _ in range(3)]

        result = self.simulate_get('/api/v1/architectures')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate schema
        for id in architectures:
            self.assertFalse(id in result.json['ids'])

    def test_many_private_architectures_auth(self):
        user_id = 'u1'
        another_user_id = 'u2'

        my_architectures = [self.create_arch_metadata(False, user_id).id for _ in range(3)]
        not_my_architectures = [self.create_arch_metadata(False, another_user_id).id for _ in range(3)]

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/architectures', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        for id in my_architectures:
            self.assertTrue(id in result.json['ids'])

        for id in not_my_architectures:
            self.assertFalse(id in result.json['ids'])

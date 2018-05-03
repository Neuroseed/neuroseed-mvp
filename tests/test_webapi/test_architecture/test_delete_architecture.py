import falcon

import metadata

from .test_architecture import TestInitAPI


class TestCreateArchitecture(TestInitAPI):
    def test_delete_architecture_no_auth(self):
        user = 'u1'
        a1 = self.create_arch_metadata(False, owner=user)

        url = '/api/v1/architecture/{id}'.format(id=a1.id)
        result = self.simulate_delete(url)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_401)

    def test_delete_architecture_auth(self):
        user = 'u1'
        a1 = self.create_arch_metadata(False, owner=user)

        token = self.create_token(user)
        headers = self.get_auth_headers(token)
        url = '/api/v1/architecture/{id}'.format(id=a1.id)
        result = self.simulate_delete(url, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

    def test_delete_others_architecture(self):
        user_id = 'u1'
        other_user_id = 'u2'
        d1 = self.create_arch_metadata(False, other_user_id)

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        url = '/api/v1/architecture/{id}'.format(id=d1.id)
        result = self.simulate_delete(url, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_404)

    def test_delete_not_exist_architecture(self):
        user = 'u1'
        token = self.create_token(user)
        headers = self.get_auth_headers(token)
        url = '/api/v1/architecture/{id}'.format(id='invalid-id')
        result = self.simulate_delete(url, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_404)

    def test_delete_published_dataset(self):
        user_id = 'u1'
        d1 = self.create_arch_metadata(True, user_id)

        d1.status = metadata.architecture.PUBLISHED
        d1.save()

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        url = '/api/v1/architecture/{id}'.format(id=d1.id)
        result = self.simulate_delete(url, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_409)

import falcon

from .test_architecture import TestInitAPI


class TestUpdateArchitecture(TestInitAPI):
    def test_update_architecture_no_auth(self):
        user_id = 'u1'
        a1 = self.create_arch_metadata(True, user_id)

        updated_title = 'updated-title'
        json = {
            'title': updated_title
        }

        url = '/api/v1/architecture/{id}'.format(id=a1.id)
        result = self.simulate_patch(url, json=json)

        self.assertEqual(result.status, falcon.HTTP_401)

    def test_update_architecture(self):
        user_id = 'u1'
        a1 = self.create_arch_metadata(True, user_id)

        updated_title = 'updated-title'
        json = {
            'title': updated_title
        }

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        url = '/api/v1/architecture/{id}'.format(id=a1.id)
        result = self.simulate_patch(url, json=json, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_204)

        result = self.simulate_get(url, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertEqual(result.json['title'], updated_title)

    def test_update_others_architecture(self):
        user_id = 'u1'
        other_user_id = 'u2'
        d1 = self.create_arch_metadata(True, other_user_id)

        updated_title = 'updated-title'
        json = {
            'title': updated_title
        }

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        url = '/api/v1/architecture/{id}'.format(id=d1.id)
        result = self.simulate_patch(url, json=json, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_404)

    def test_update_architecture_not_exist(self):
        user_id = 'u1'
        architecture_id = 'not-exist-dataset-id'

        updated_title = 'updated-title'
        json = {
            'title': updated_title
        }

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        url = '/api/v1/architecture/{id}'.format(id=architecture_id)
        result = self.simulate_patch(url, json=json, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_404)

import falcon

from .test_model import TestInitAPI


class TestUpdateModel(TestInitAPI):
    def test_update_model_no_auth(self):
        user_id = 'u1'
        meta = self.create_model_metadata(True, user_id)

        updated_title = 'updated-title'
        json = {
            'title': updated_title
        }

        url = '/api/v1/model/{id}'.format(id=meta.id)
        result = self.simulate_patch(url, json=json)

        self.assertEqual(result.status, falcon.HTTP_401)

    def test_update_model(self):
        user_id = 'u1'
        meta = self.create_model_metadata(True, user_id)

        updated_title = 'updated-title'
        json = {
            'title': updated_title
        }

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        url = '/api/v1/model/{id}'.format(id=meta.id)
        result = self.simulate_patch(url, json=json, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_204)

        result = self.simulate_get(url, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertEqual(result.json['title'], updated_title)

    def test_update_others_model(self):
        user_id = 'u1'
        other_user_id = 'u2'
        meta = self.create_model_metadata(True, other_user_id)

        updated_title = 'updated-title'
        json = {
            'title': updated_title
        }

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        url = '/api/v1/model/{id}'.format(id=meta.id)
        result = self.simulate_patch(url, json=json, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_404)

    def test_update_model_not_exist(self):
        user_id = 'u1'
        model_id = 'not-exist-dataset-id'

        updated_title = 'updated-title'
        json = {
            'title': updated_title
        }

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        url = '/api/v1/model/{id}'.format(id=model_id)
        result = self.simulate_patch(url, json=json, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_404)

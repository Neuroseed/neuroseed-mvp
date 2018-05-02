import falcon

from .test_model import TestInitAPI


class TestModel(TestInitAPI):
    def test_update_model(self):
        m1 = self.create_model_metadata(True, 'u1')

        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        url = '/api/v1/model/{id}'.format(id=m1.id)
        result = self.simulate_post(url, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_400)

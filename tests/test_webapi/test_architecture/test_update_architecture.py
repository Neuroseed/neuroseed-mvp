import falcon

from .test_architecture import TestInitAPI


class TestUpdateArchitecture(TestInitAPI):
    def test_update_architecture_no_auth(self):
        a1 = self.create_arch_metadata(True, 'u1')
        json = {
            'title': 'title',
            'architecture': {
                'layers': []
            }
        }
        url = '/api/v1/architecture/{id}'.format(id=a1.id)
        result = self.simulate_post(url, json=json)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_401)

    def test_update_architecture_auth(self):
        a1 = self.create_arch_metadata(True, 'u1')
        json = {
            'title': 'title',
            'architecture': {
                'layers': [
                    {'name': 'Flatten'}
                ]
            }
        }
        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        url = '/api/v1/architecture/{id}'.format(id=a1.id)
        result = self.simulate_post(url, json=json, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

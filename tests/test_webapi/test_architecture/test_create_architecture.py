import falcon

from .test_architecture import TestInitAPI


class TestCreateArchitecture(TestInitAPI):
    def test_create_architecture_no_auth(self):
        json = {}
        result = self.simulate_post('/api/v1/architecture', json=json)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_401)

    def test_create_architecture_auth(self):
        json = {
            'title': 'title',
            'architecture': {
                'layers': [
                    {
                        "name": "Dense",
                        "config": {
                            "units": 3
                        }
                    }
                ]
            }
        }
        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_post('/api/v1/architecture', json=json, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

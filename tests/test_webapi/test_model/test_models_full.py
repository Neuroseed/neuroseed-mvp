import falcon

from .test_model import TestInitAPI


class TestModelsFull(TestInitAPI):
    def test_get_empty(self):
        result = self.simulate_get('/api/v1/models/full')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

    def test_get_one(self):
        a1 = self.create_model_metadata(True, 'u1')

        result = self.simulate_get('/api/v1/models/full')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        models = result.json['models']
        self.assertEqual(len(models), 1)

        self.assertEqual(models[0]['id'], a1.id)

    def test_get_many_no_auth(self):
        number = 5
        [self.create_model_metadata(True, 'u1') for _ in range(number)]

        result = self.simulate_get('/api/v1/models/full')

        # validate codes
        self.assertEqual(result.status, falcon.HTTP_200)

        models = result.json['models']
        self.assertEqual(len(models), number)

    def test_get_many_auth(self):
        number = 5
        [self.create_model_metadata(False, 'u1') for _ in range(number)]
        [self.create_model_metadata(False, 'u2') for _ in range(number)]

        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/models/full', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        models = result.json['models']
        self.assertEqual(len(models), number)

    def test_query_slice_on_border(self):
        number = 20
        [self.create_model_metadata(True, 'u1') for _ in range(number)]

        from_ = 10
        n = 20
        query_string = 'from={f}&number={n}'.format(f=from_, n=n)
        result = self.simulate_get('/api/v1/models/full', query_string=query_string)

        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertEqual(len(result.json['models']), number - from_)

    def test_query_invalid_slice(self):
        number = 5
        [self.create_model_metadata(True, 'u1') for _ in range(number)]

        query_string = 'from=-2&number=3'
        result = self.simulate_get('/api/v1/models/full', query_string=query_string)
        self.assertEqual(result.status, falcon.HTTP_400)

        query_string = 'from=1&number=-3'
        result = self.simulate_get('/api/v1/models/full', query_string=query_string)
        self.assertEqual(result.status, falcon.HTTP_400)

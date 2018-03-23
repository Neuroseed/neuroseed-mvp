import falcon
from falcon import testing
import webapi
import uuid
import metadata
import jwt
from mongoengine import connect


class TestInitAPI(testing.TestCase):
    def create_token(self, user_id):
        payload = {
            'user_id': user_id
        }
        token = jwt.encode(payload, self.SECRET_KEY, algorithm='HS256').decode('utf-8')
        return token

    def get_auth_headers(self, token):
        return {
            'Authorization': 'Bearer {token}'.format(token=token)
        }

    def setUp(self):
        super().setUp()

        connect('metaddata', host='mongomock://localhost', alias='metadata')
        config = {
            "auth_key_file": "config/auth.key",
            "celery_config": "config/celery_config.json",
            "metadata_config": {},
        }
        self.SECRET_KEY = open(config["auth_key_file"]).read()
        self.app = webapi.main(config)


class TestArchitecture(TestInitAPI):
    def tearDown(self):
        metadata.DatasetMetadata.objects.all().delete()

    def create_arch_metadata(self, is_public, owner):
        architecture = metadata.ArchitectureMetadata()
        architecture.id = str(uuid.uuid4())
        architecture.is_public = is_public
        architecture.owner = owner
        architecture.title = 'title'
        architecture.architecture = {'layers': []}
        architecture.save()

        return architecture

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

    def test_get_architecture(self):
        result = self.simulate_get('/api/v1/architecture')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_404)

    def test_get_architecture_does_not_exist(self):
        result = self.simulate_get('/api/v1/architecture/arch-id')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_404)

    def test_get_public_architecture(self):
        a1 = self.create_arch_metadata(True, 'u1')
        result = self.simulate_get('/api/v1/architecture/{id}'.format(id=a1.id))

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertEqual(a1.id, result.json['id'])

    def test_get_private_architecture(self):
        a1 = self.create_arch_metadata(False, 'u1')
        result = self.simulate_get('/api/v1/architecture/{id}'.format(id=a1.id))

        # validate code
        self.assertEqual(result.status, falcon.HTTP_404)

    def test_get_private_architecture_auth(self):
        a1 = self.create_arch_metadata(False, 'u1')

        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/architecture/{id}'.format(id=a1.id), headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertEqual(a1.id, result.json['id'])

    def test_create_architecture_no_auth(self):
        json = {}
        result = self.simulate_post('/api/v1/architecture', json=json)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_401)

    def test_create_architecture_auth(self):
        json = {
            'title': 'title',
            'architecture': {
                'layers': []
            }
        }
        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_post('/api/v1/architecture', json=json, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

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
                'layers': []
            }
        }
        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        url = '/api/v1/architecture/{id}'.format(id=a1.id)
        result = self.simulate_post(url, json=json, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

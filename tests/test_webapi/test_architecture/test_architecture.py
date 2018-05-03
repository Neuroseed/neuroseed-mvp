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

    def tearDown(self):
        metadata.ArchitectureMetadata.objects.all().delete()

    def create_arch_metadata(self, is_public, owner):
        architecture = metadata.ArchitectureMetadata()
        architecture.id = str(uuid.uuid4())
        architecture.is_public = is_public
        architecture.owner = owner
        architecture.title = 'title'
        architecture.architecture = {'layers': []}
        architecture.save()

        return architecture


class TestArchitecture(TestInitAPI):
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

    def test_get_other_public_architecture_with_auth(self):
        user_1 = 'u1'
        user_2 = 'u2'

        not_my_public_architecture = self.create_arch_metadata(True, user_2)

        token = self.create_token(user_1)
        headers = self.get_auth_headers(token)
        url = '/api/v1/architecture/{id}'.format(id=not_my_public_architecture.id)
        result = self.simulate_get(url, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertTrue(not_my_public_architecture.id, result.json['id'])

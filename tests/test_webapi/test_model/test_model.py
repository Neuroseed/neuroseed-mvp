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
        metadata.DatasetMetadata.objects.all().delete()
        metadata.ArchitectureMetadata.objects.all().delete()
        metadata.ModelMetadata.objects.all().delete()

    def create_dataset_metadata(self, is_public, owner):
        dataset = metadata.DatasetMetadata()
        dataset.is_public = is_public
        dataset.base.owner = owner
        dataset.id = str(uuid.uuid4())
        dataset.url = dataset.id
        dataset.base.title = 'title'
        dataset.save()

        return dataset

    def create_arch_metadata(self, is_public, owner):
        architecture = metadata.ArchitectureMetadata()
        architecture.id = str(uuid.uuid4())
        architecture.is_public = is_public
        architecture.owner = owner
        architecture.title = 'title'
        architecture.architecture = {'layers': []}
        architecture.save()

        return architecture

    def create_model_metadata(self, is_public, owner):
        model = metadata.ModelMetadata()
        model.id = str(uuid.uuid4())
        model.url = model.id
        model.is_public = is_public
        model.base.owner = owner
        model.base.title = 'title'
        model.base.architecture = self.create_arch_metadata(is_public, owner)
        model.base.dataset = self.create_dataset_metadata(is_public, owner)
        model.save()

        return model


class TestModel(TestInitAPI):
    def test_get_one_model_no_auth(self):
        m1 = self.create_model_metadata(True, 'u1')

        url = '/api/v1/model/{id}'.format(id=m1.id)
        result = self.simulate_get(url)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate id
        self.assertEqual(result.json['id'], m1.id)

    def test_get_one_private_model_no_auth(self):
        m1 = self.create_model_metadata(False, 'u1')

        url = '/api/v1/model/{id}'.format(id=m1.id)
        result = self.simulate_get(url)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_404)

    def test_get_one_model_auth(self):
        m1 = self.create_model_metadata(False, 'u1')

        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        url = '/api/v1/model/{id}'.format(id=m1.id)
        result = self.simulate_get(url, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate id
        self.assertEqual(result.json['id'], m1.id)

    def test_get_other_public_model_with_auth(self):
        user_1 = 'u1'
        user_2 = 'u2'

        not_my_public_model = self.create_model_metadata(True, user_2)

        token = self.create_token(user_1)
        headers = self.get_auth_headers(token)
        url = '/api/v1/model/{id}'.format(id=not_my_public_model.id)
        result = self.simulate_get(url, headers=headers)

        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertTrue(not_my_public_model.id, result.json['id'])

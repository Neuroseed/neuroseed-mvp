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


class TestModels(TestInitAPI):
    def tearDown(self):
        metadata.DatasetMetadata.objects.all().delete()

    def create_task_metadata(self, owner):
        document = {
            'command': 'command',
            'config': {}
        }

        task = metadata.TaskMetadata(**document)
        task.id = str(uuid.uuid4())
        task.owner = owner
        task.save()

        return task

    def test_get_datasets_no_auth(self):
        result = self.simulate_get('/api/v1/tasks')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_401)

    def test_get_datasets_schema_auth(self):
        token = self.create_token("u1")
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/tasks', headers=headers)

        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertEqual(list(result.json.keys()), ['ids'])

    def test_many_tasks_auth(self):
        user_id = 'u1'
        tasks = [self.create_task_metadata(user_id).id for _ in range(3)]

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/tasks', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        # validate schema
        for id in tasks:
            self.assertTrue(id in result.json['ids'])

    def test_many_others_tasks_auth(self):
        user_id = 'u1'
        another_user_id = 'u2'

        my_tasks = [self.create_task_metadata(user_id).id for _ in range(3)]
        not_my_tasks = [self.create_task_metadata(another_user_id).id for _ in range(3)]

        token = self.create_token(user_id)
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/tasks', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        for id in my_tasks:
            self.assertTrue(id in result.json['ids'])

        for id in not_my_tasks:
            self.assertFalse(id in result.json['ids'])

    def test_get_task_no_auth(self):
        result = self.simulate_get('/api/v1/task')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_401)

    def test_get_task_does_not_exist(self):
        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/task/some-task-id', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_404)

    def task_get_task_others(self):
        t1 = self.create_task_metadata('u2')

        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        url = '/api/v1/task/{id}'.format(id=t1.id)
        result = self.simulate_get(url, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_404)

    def test_create_task_no_auth(self):
        json = {
            'command': 'command',
            'config': {}
        }
        result = self.simulate_post('/api/v1/task', json=json)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_401)

    def test_create_task(self):
        json = {
            'command': 'command',
            'config': {}
        }
        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_post('/api/v1/task', json=json, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

    def test_create_task_invalid_schema(self):
        json = {
            'command': 'command',
            'config': {},
            'wrong_field': 1
        }
        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_post('/api/v1/task', json=json, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_400)  # Bad Request

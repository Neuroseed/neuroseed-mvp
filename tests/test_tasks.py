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
        metadata.TaskMetadata.objects.all().delete()

    def create_task_metadata(self, owner):
        document = {
            'command': 'command',
            'config': {}
        }

        task = metadata.TaskMetadata(**document)
        task.id = str(uuid.uuid4())
        task.owner = owner
        task.command = metadata.task.MODEL_TRAIN
        task.save()

        return task


class TestModels(TestInitAPI):
    def test_get_tasks_no_auth(self):
        result = self.simulate_get('/api/v1/tasks')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_401)

    def test_get_tasks_schema_auth(self):
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
            'command': metadata.task.MODEL_TRAIN,
            'config': {}
        }
        result = self.simulate_post('/api/v1/task', json=json)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_401)

    def test_create_task(self):
        json = {
            'command': metadata.task.MODEL_TRAIN,
            'config': {}
        }
        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_post('/api/v1/task', json=json, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

    def test_create_task_invalid_schema(self):
        json = {
            'command': metadata.task.MODEL_TRAIN,
            'config': {},
            'wrong_field': 1
        }
        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_post('/api/v1/task', json=json, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_400)  # Bad Request


class TestTasksFull(TestInitAPI):
    def test_get_tasks_no_auth(self):
        result = self.simulate_get('/api/v1/tasks/full')

        # validate code
        self.assertEqual(result.status, falcon.HTTP_401)

    def test_get_one(self):
        t1 = self.create_task_metadata('u1')

        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/tasks/full', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        models = result.json['tasks']
        self.assertEqual(len(models), 1)

        self.assertEqual(models[0]['id'], t1.id)

    def test_get_many_no_auth(self):
        number = 5
        [self.create_task_metadata('u1') for _ in range(number)]

        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/tasks/full', headers=headers)

        # validate codes
        self.assertEqual(result.status, falcon.HTTP_200)

        tasks = result.json['tasks']
        self.assertEqual(len(tasks), number)

    def test_get_many_auth(self):
        number = 5
        [self.create_task_metadata('u1') for _ in range(number)]
        [self.create_task_metadata('u2') for _ in range(number)]

        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/tasks/full', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        tasks = result.json['tasks']
        self.assertEqual(len(tasks), number)


class TestTasksNumber(TestInitAPI):
    def test_get_number_of_empty(self):
        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/tasks/number', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        self.assertEqual(result.json, 0)

    def test_get_number_one(self):
        t1 = self.create_task_metadata('u1')

        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/tasks/number', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        self.assertEqual(result.json, 1)

    def test_get_number_many(self):
        number = 15
        tasks = [self.create_task_metadata('u1') for _ in range(number)]

        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/tasks/number', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        self.assertEqual(result.json, number)

    def test_get_number_many_auth(self):
        number = 5
        tasks = [self.create_task_metadata('u1') for _ in range(number)]
        tasks = [self.create_task_metadata('u2') for _ in range(number)]

        token = self.create_token('u1')
        headers = self.get_auth_headers(token)
        result = self.simulate_get('/api/v1/tasks/number', headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        self.assertEqual(result.json, number)

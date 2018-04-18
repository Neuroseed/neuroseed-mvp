import time

import jwt
import falcon
from falcon import testing
from mongoengine import connect

import webapi
import storage
import metadata
import manager

from ..test_worker.utils import get_cifar10


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

        storage.from_config('config/storage_config.json')

        manager.from_config({
            'embedded_worker': True
        })

    def tearDown(self):
        metadata.DatasetMetadata.objects.all().delete()
        metadata.ArchitectureMetadata.objects.all().delete()
        metadata.ModelMetadata.objects.all().delete()

    def create_cifar10_dataset(self):
        with metadata.DatasetMetadata().save_context() as dataset:
            dataset.base.owner = 'u1'
            dataset.base.title = 'cifar10'

        with open(get_cifar10(0.1), 'rb') as f:
            manager.save_dataset(dataset, f)

        return dataset

    def create_architecture(self):
        architecture = {
            "layers": [
                {
                    "name": "Conv2D",
                    "config": {
                        "filters": 32,
                        "kernel_size": [3, 3]
                    }
                },
                {
                    "name": "MaxPooling2D",
                    "config": {
                        "pool_size": [2, 2]
                    }
                },
                {
                    "name": "Conv2D",
                    "config": {
                        "filters": 32,
                        "kernel_size": [3, 3]
                    }
                },
                {"name": "Flatten"},
                {
                    "name": "Dense",
                    "config": {
                        "units": 10
                    }
                }
            ]
        }

        with metadata.ArchitectureMetadata().save_context() as meta:
            meta.owner = 'u1'
            meta.title = 'cifar10'
            meta.architecture = architecture

        return meta

    def create_model(self, dataset, architecture):
        with metadata.ModelMetadata().save_context() as model:
            model.base.owner = 'u1'
            model.base.title = 'cifar10 model'
            model.base.dataset = dataset
            model.base.architecture = architecture

        return model

    def test_train_no_exceptions(self):
        dataset = self.create_cifar10_dataset()
        architecture = self.create_architecture()
        model = self.create_model(dataset, architecture)

        json = {
            "epochs": 1,
            "optimizer": {
                "name": "SGD"
            },
            "loss": "categorical_crossentropy"
        }

        token = self.create_token("u1")
        headers = self.get_auth_headers(token)
        url = '/api/v1/model/{id}/train'.format(id=model.id)
        result = self.simulate_post(url, json=json, headers=headers)

        # validate code
        self.assertEqual(result.status, falcon.HTTP_200)

        task_id = result.json['id']

        url = '/api/v1/model/train/{tid}'.format(tid=task_id)
        result = self.simulate_get(url, json=json, headers=headers)

        # validate code
        for i in range(5):
            self.assertEqual(result.status, falcon.HTTP_200)
            time.sleep(1)

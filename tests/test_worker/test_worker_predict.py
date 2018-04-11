import unittest
from mongoengine import connect

import metadata
import manager
import storage
import worker

from .utils import get_cifar10


class TestWorkerTestOnCIFAR10(unittest.TestCase):
    def setUp(self):
        super().setUp()

        connect('metaddata', host='mongomock://localhost', alias='metadata')

        storage.from_config('config/storage_config.json')

    def tearDown(self):
        metadata.DatasetMetadata.objects.all().delete()
        metadata.ArchitectureMetadata.objects.all().delete()
        metadata.ModelMetadata.objects.all().delete()

    def create_cifar10_dataset(self):
        with metadata.DatasetMetadata().save_context() as dataset:
            dataset.base.owner = 'u1'
            dataset.base.title = 'cifar10'

        with open(get_cifar10(), 'rb') as f:
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

    def train_model(self):
        dataset = self.create_cifar10_dataset()
        architecture = self.create_architecture()
        model = self.create_model(dataset, architecture)

        with metadata.TaskMetadata().save_context() as task:
            task.owner = 'u1'
            task.command = 'model.train'
            task.config = {
                'dataset': dataset.id,
                'model': model.id,
                'epoch': 1,
                'optimizer': {
                    "name": "SGD"
                },
                "loss": "categorical_crossentropy"
            }

        worker.tasks.train_on_task(task)

        return dataset, architecture, model, task

    def test_test_model(self):
        dataset, architecture, model, task = self.train_model()

        with metadata.TaskMetadata().save_context() as task:
            task.owner = 'u1'
            task.command = 'model.test'
            task.config = {
                'dataset': dataset.id,
                'model': model.id
            }

        worker.tasks.predict_on_task(task)

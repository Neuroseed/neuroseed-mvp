import falcon

from ..schema import dataset
from ..schema import architecture
from ..schema import model
from ..schema import model_train
from ..schema import model_test
from ..schema import model_predict
from ..schema import task
from ..schema import layers


__all__ = [
    'SchemaModelLayersResource',
    'SchemaDatasetResource',
    'SchemaArchitectureResource',
    'SchemaModelResource',
    'SchemaModelTrainResource',
    'SchemaModelTestResource',
    'SchemaTaskResource',
    'SchemaModelPredictResource'
]


class SchemaModelLayersResource:
    auth = {
        'exempt_methods': ['GET']
    }

    def __init__(self, enable_new_layer=True):
        self.enable_new_layer = enable_new_layer

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

        if self.enable_new_layer:
            resp.media = layers.LAYERS
        else:
            resp.media = layers.OLD_LAYERS


class SchemaDatasetResource:
    auth = {
        'exempt_methods': ['GET']
    }

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = dataset.CREATE_DATASET_SCHEMA


class SchemaArchitectureResource:
    auth = {
        'exempt_methods': ['GET']
    }

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = architecture.ARCHITECTURE_SCHEMA


class SchemaModelResource:
    auth = {
        'exempt_methods': ['GET']
    }

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = model.MODEL_SCHEMA


class SchemaTaskResource:
    auth = {
        'exempt_methods': ['GET']
    }

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = task.TASK_SCHEMA


class SchemaModelTrainResource:
    auth = {
        'exempt_methods': ['GET']
    }

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = model_train.MODEL_TRAIN_SCHEMA


class SchemaModelTestResource:
    auth = {
        'exempt_methods': ['GET']
    }

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = model_test.MODEL_TEST_SCHEMA


class SchemaModelPredictResource:
    auth = {
        'exempt_methods': ['GET']
    }

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = model_predict.MODEL_PREDICT_SCHEMA

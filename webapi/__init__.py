import logging

import falcon
from falcon import media
from falcon_auth import JWTAuthBackend, FalconAuthMiddleware

from .resources import *

__version__ = '0.1.0'

logger = logging.getLogger(__name__)


class NeuroseedAuthMiddleware(FalconAuthMiddleware):
    """
    Resource auth schema:
    auth = {
        inherit FalconAuthMiddleware auth schema,
        'optional_routes': []
        'optional_methods': []
    }
    """

    def __init__(self, backend, exempt_routes=None, exempt_methods=None
, optional_routes=None, optional_methods=None):
        super().__init__(backend, exempt_routes, exempt_methods)

        self.optional_routes = list(optional_routes or [])
        self.optional_methods = list(optional_methods or [])

    def process_resource(self, req, resp, resource, *args, **kwargs):
        auth_setting = self._get_auth_settings(req, resource)
        try:
            super().process_resource(req, resp, resource, *args, **kwargs)
        except falcon.HTTPUnauthorized:
            optional_routes = tuple(self.optional_routes) + tuple(auth_setting.get('optional_routes', ()))
            optional_methods = tuple(self.optional_methods) + tuple(auth_setting.get('optional_methods', ()))

            if req.path in optional_routes or \
               req.method in optional_methods:
                req.context['user'] = None
            else:
                raise


class TextPlainHandler(media.BaseHandler):
    """
    Обработчик текстовых данных типа
    MIME text/plain
    """

    def serialize(self, obj):
        return obj

    def deserialize(self, raw):
        return raw


def configure_api_v1(api, auth):
    BASE = '/api/v1/'

    # dataset operations
    dataset_resource = DatasetResource()
    api.add_route(BASE + 'dataset', dataset_resource)
    api.add_route(BASE + 'dataset/{id}', dataset_resource)

    # list of datasets
    datasets_resource = DatasetsResource()
    api.add_route(BASE + 'datasets', datasets_resource)
    auth.optional_routes.append(BASE + 'datasets')

    # architecture operations
    architecture_resource = ArchitectureResource()
    api.add_route(BASE + 'architecture', architecture_resource)
    api.add_route(BASE + 'architecture/{id}', architecture_resource)
    auth.optional_routes.append(BASE + 'architecture/{id}')

    # list of architectures
    architectures_resource = ArchitecturesResource()
    api.add_route(BASE + 'architectures', architectures_resource)
    auth.optional_routes.append(BASE + 'architectures')

    # model operation
    model_resource = ModelResource()
    api.add_route(BASE + 'model', model_resource)
    api.add_route(BASE + 'model/{id}', model_resource)

    model_train_resource = ModelTrainResource()
    api.add_route(BASE + 'model/{id}/train', model_train_resource)

    model_test_resource = ModelTestResource()
    api.add_route(BASE + 'model/{id}/test', model_test_resource)

    model_predict_resource = ModelPredictResource()
    api.add_route(BASE + 'model/{id}/predict', model_predict_resource)

    model_predict_status_resource = ModelPredictStatusResource()
    api.add_route(BASE + 'model/predict/{tid}', model_predict_status_resource)

    model_predict_result_resource = ModelPredictResult()
    api.add_route(BASE + 'model/predict/{tid}/resource', model_predict_result_resource)

    # list of models
    models_resource = ModelsResource()
    api.add_route(BASE + 'models', models_resource)
    auth.optional_routes.append(BASE + 'models')

    # task operation
    task_resource = TaskResource()
    api.add_route(BASE + 'task/{id}', task_resource)
    api.add_route(BASE + 'task', task_resource)

    # tasks list
    tasks_resource = TasksResource()
    api.add_route(BASE + 'tasks', tasks_resource)

    logger.debug('api v1 initialized')


def main(config=None):
    key_file = config['auth_key_file']

    with open(key_file) as f:
        secret_key = f.read()

    user_loader = lambda payload: payload['user_id']
    jwt_auth_backend = JWTAuthBackend(
        user_loader,
        secret_key,
        required_claims=['user_id'],
        auth_header_prefix='Bearer')
    auth_middleware = NeuroseedAuthMiddleware(jwt_auth_backend)
    middleware = [auth_middleware]

    api = falcon.API(middleware=middleware)
    extra_handlers = {
        'text/plain': TextPlainHandler()
    }
    api.req_options.media_handlers.update(extra_handlers)

    configure_api_v1(api, auth_middleware)

    return api

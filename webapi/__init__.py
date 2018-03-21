import logging

import falcon
from falcon import media
from falcon_auth import JWTAuthBackend, FalconAuthMiddleware

from .resources import *

__version__ = '0.1.0'

logger = logging.getLogger(__name__)


# TODO: FIX FALCON BUG AND DELETE THIS MONKEY PATH !!!
def _read(self, size, target):
    """Helper function for proxing reads to the underlying stream.
    Args:
        size (int): Maximum number of bytes to read. Will be
            coerced, if None or -1, to the number of remaining bytes
            in the stream. Will likewise be coerced if greater than
            the number of remaining bytes, to avoid making a
            blocking call to the wrapped stream.
        target (callable): Once `size` has been fixed up, this function
            will be called to actually do the work.
    Returns:
        bytes: Data read from the stream, as returned by `target`.
    """

    # NOTE(kgriffs): Default to reading all remaining bytes if the
    # size is not specified or is out of bounds. This behaves
    # similarly to the IO streams passed in by non-wsgiref servers.
    if (size is None or size == -1 or size > self._bytes_remaining):
        size = self._bytes_remaining

    raw = target(size)
    self._bytes_remaining -= len(raw)
    return raw

import hashlib
if hashlib.sha256(falcon.request_helpers.BoundedStream._read.__code__.co_code).hexdigest() != 'f01e0ef4b334be2ac60c8740a675223da618257bb0ae25a7a29bfbdd812be3a7':
    raise ValueError('Falcon fix bug')

falcon.request_helpers.BoundedStream._read = _read


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


class NothingHandler(media.BaseHandler):
    """
    Обработчик данных без преобразования
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


def main():
    SECRET_KEY = 'secret'
    user_loader = lambda payload: payload['user_id']
    jwt_auth_backend = JWTAuthBackend(
        user_loader,
        SECRET_KEY,
        required_claims=['user_id'],
        auth_header_prefix='Bearer')
    auth_middleware = NeuroseedAuthMiddleware(jwt_auth_backend)
    middleware = [auth_middleware]

    api = falcon.API(middleware=middleware)
    extra_handlers = {
        #'multipart/form-data': NothingHandler()
    }
    api.req_options.media_handlers.update(extra_handlers)

    configure_api_v1(api, auth_middleware)

    return api

import logging
import json

import falcon
from falcon_auth import JWTAuthBackend
from falcon_cors import CORS

import metadata
import manager
import storage
from . import apiv1
from .authmiddleware import NeuroseedAuthMiddleware
from .loggingmiddleware import LoggingMidleware
from . import serializers
from .helpers import init_logging
from .version import __version__

# fix falcon bug
from . import patch


logger = logging.getLogger(__name__)


def from_config(config=None):
    if type(config) is str:
        with open(config) as f:
            config = json.load(f)
    elif type(config) is dict:
        pass
    elif config is None:
        return {}

    metadata_config = config.get('metadata_config', None)
    if metadata_config:
        metadata.from_config(metadata_config)

    storage_config = config.get('storage_config', None)
    if storage_config:
        storage.from_config(storage_config)

    manager_config = config.get('manager_config', None)
    if manager_config:
        manager.from_config(manager_config)

    return config


def get_auth_key(key_file):
    with open(key_file) as f:
        secret_key = f.read().strip()

    return secret_key


def get_auth_middleware(secret_key=None, key_file=None):
    if type(key_file) is str:
        secret_key = get_auth_key(key_file)
    elif not type(secret_key) is str:
        raise TypeError('type of secret_key or key_file must be str')

    user_loader = lambda payload: payload['user_id']
    jwt_auth_backend = JWTAuthBackend(
        user_loader,
        secret_key,
        required_claims=['user_id'],
        auth_header_prefix='Bearer')
    auth_middleware = NeuroseedAuthMiddleware(jwt_auth_backend)

    return auth_middleware


def get_cors_middleware():
    cors = CORS(
        allow_all_origins=True,
        allow_credentials_all_origins=True,
        allow_all_methods=True,
        allow_all_headers=True)

    return cors.middleware


def main(config):
    if not type(config) is dict:
        raise TypeError('type of config must be dict')

    middlewares = []

    key_file = config['auth_key_file']
    auth_middleware = get_auth_middleware(key_file=key_file)
    middlewares.append(auth_middleware)

    # Cross-origin resource sharing - "совместное использование ресурсов между разными источниками"
    use_cors = config.get('use_cors', True)
    if use_cors:
        logger.debug('User CORS')
        cors = get_cors_middleware()
        middlewares.append(cors)

    use_extend_logging = config.get('use_extend_logging', True)
    if use_extend_logging:
        logging.debug('Use extend falcon logging')
        logging_middleware = LoggingMidleware(logger)
        middlewares.append(logging_middleware)

    api = falcon.API(middleware=middlewares)

    api.set_error_serializer(serializers.falcon_error_serializer)

    apiv1.configure_api_v1(api, auth_middleware)

    return api


def serve_forever(api, config):
    from gevent import pywsgi

    host = config['host']
    port = config['port']

    httpd = pywsgi.WSGIServer((host, port), api)
    logging.debug('Start server on {}:{}'.format(host, port))
    httpd.serve_forever()

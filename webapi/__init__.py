import logging
import json

import falcon
from falcon_auth import JWTAuthBackend
from falcon_cors import CORS

import metadata
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


def from_config(config_file=None):
    if type(config_file) is str:
        with open(config_file) as f:
            config = json.load(f)
    elif type(config_file) is dict:
        config = config_file
    elif config_file is None:
        return {}

    metadata_config = config.get('metadata_config', None)
    if metadata_config:
        metadata.from_config(metadata_config)

    storage_config = config.get('storage_config', None)
    if storage_config:
        storage.from_config(storage_config)

    return config


def get_auth_key(key_file):
    with open(key_file) as f:
        secret_key = f.read().strip()

    return secret_key


def get_auth_middleware(secret_key):
    user_loader = lambda payload: payload['user_id']
    jwt_auth_backend = JWTAuthBackend(
        user_loader,
        secret_key,
        required_claims=['user_id'],
        auth_header_prefix='Bearer')
    auth_middleware = NeuroseedAuthMiddleware(jwt_auth_backend)

    return auth_middleware


def main(config):
    if not type(config) is dict:
        raise TypeError('type of config must be dict')

    key_file = config['auth_key_file']
    secret_key = get_auth_key(key_file)

    middlewares = []

    auth_middleware = get_auth_middleware(secret_key)
    middlewares.append(auth_middleware)

    # Cross-origin resource sharing - "совместное использование ресурсов между разными источниками"
    use_cors = config.get('use_cors', True)
    if use_cors:
        cors = CORS(
            allow_all_origins=True,
            allow_credentials_all_origins=True,
            allow_all_methods=True,
            allow_all_headers=True)
        middlewares.append(cors.middleware)

    use_extend_logging = config.get('use_extend_logging', True)
    if use_extend_logging:
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

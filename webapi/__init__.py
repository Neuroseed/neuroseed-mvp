import sys
import os
import logging
import json

import falcon
from falcon import media
from falcon_auth import JWTAuthBackend

import metadata
import storage
from . import apiv1
from .authmiddleware import NeuroseedAuthMiddleware


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
    logger.warning('Falcon fix BoundedStream.readline bug')

falcon.request_helpers.BoundedStream._read = _read


class NothingHandler(media.BaseHandler):
    """
    Обработчик данных без преобразования
    """

    def serialize(self, obj):
        return obj

    def deserialize(self, raw):
        return raw


def init_logging():
    def excepthook(type, value, traceback):
        logging.critical('Uncaught exception',
                         exc_info=(type, value, traceback))

        sys.__excepthook__(type, value, traceback)

        sys.exit(1)

    sys.excepthook = excepthook

    if not os.path.isdir('logs'):
        os.mkdir('logs')

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    file_handler = logging.FileHandler('logs/log-web-api.txt', mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    logging.warning('Start logging')


def from_config(config_file):
    if type(config_file) is str:
        with open(config_file) as f:
            config = json.load(f)
    elif type(config_file) is dict:
        config = config_file

    metadata_config = config['metadata_config']
    metadata.from_config(metadata_config)

    storage_config = config['storage_config']
    storage.from_config(storage_config)

    return config


def main(config):
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
        #'multipart/form-data': NothingHandler()
    }
    api.req_options.media_handlers.update(extra_handlers)

    apiv1.configure_api_v1(api, auth_middleware)

    return api


def serve_forever(api, config):
    from gevent import pywsgi

    host = config['host']
    port = config['port']

    httpd = pywsgi.WSGIServer((host, port), api)
    logging.debug('Start server on {}:{}'.format(host, port))
    httpd.serve_forever()

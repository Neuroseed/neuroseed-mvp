import sys
import os
import json
import logging

import webapi
import metadata
import storage


def excepthook(type, value, traceback):
    logging.critical('Uncaught exception',
                     exc_info=(type, value, traceback))

    sys.__excepthook__(type, value, traceback)

    sys.exit(1)


sys.excepthook = excepthook


def init_logging():
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

init_logging()

api = webapi.main()


def serve_forever():
    with open('config/falcon_config.json') as f:
        config = json.load(f)

    host = config['host']
    port = config['port']

    httpd = simple_server.make_server(host, port, api)
    logging.debug('Start server on {}:{}'.format(host, port))
    httpd.serve_forever()


if __name__ == '__main__':
    from wsgiref import simple_server

    metadata.from_config('config/metadata_config.json')
    storage.from_config('config/storage_config.json')

    serve_forever()


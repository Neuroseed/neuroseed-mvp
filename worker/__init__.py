import sys
import json

from .tasks import *
from .app import app

CONFIG = {}


def celery_from_config(config_file):
    if type(config_file) is str:
        with open(config_file) as f:
            config = json.load(f)
    elif type(config_file) is dict:
        config = config_file

    app.config_from_object(config)


def from_config(config):
    global CONFIG

    if type(config) is str:
        with open(config) as f:
            config = json.load(f)
    elif type(config) is dict:
        pass
    else:
        raise TypeError('type of config must be str or dict')

    CONFIG = config


def main(*args, **kwargs):
    celery_config = CONFIG['celery_config']
    celery_from_config(celery_config)

    metadata_config = CONFIG['metadata_config']
    metadata.from_config(metadata_config)

    storage_config = CONFIG['storage_config']
    storage.from_config(storage_config)

    log_level = CONFIG['log_level']
    sys.argv.extend(['-l', log_level])
    sys.argv.append('--logfile=logs/%p-%i.log')
    sys.argv.append('--autoscale=10,1')

    app.worker_main(*args, **kwargs)

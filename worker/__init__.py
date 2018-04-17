import sys
import json

import keras.backend as K
import tensorflow as tf

from .tasks import *
from .app import app


def celery_from_config(config_file):
    if type(config_file) is str:
        with open(config_file) as f:
            config = json.load(f)
    elif type(config_file) is dict:
        config = config_file

    app.config_from_object(config)


def from_config(config_file):
    if type(config_file) is str:
        with open(config_file) as f:
            config = json.load(f)
    elif type(config_file) is dict:
        config = config_file

    celery_config = config['celery_config']
    celery_from_config(celery_config)

    metadata_config = config['metadata_config']
    metadata.from_config(metadata_config)

    storage_config = config['storage_config']
    storage.from_config(storage_config)

    log_level = config['log_level']
    sys.argv.extend(['-l', log_level])
    sys.argv.append('--autoscale=10,1')


def start_task(task):
    with tf.Session(graph=tf.Graph()) as sess:
        K.set_session(sess)

        if task.command == 'model.train':
            train_on_task(task)
        if task.command == 'model.test':
            test_on_task(task)
        if task.command == 'model.predict':
            predict_on_task(task)


def main(*args, **kwargs):
    app.worker_main(*args, **kwargs)

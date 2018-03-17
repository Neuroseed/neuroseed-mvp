import os
from os import path
import json


def from_config(config_path):
    global HOME_DIR

    with open(config_path) as f:
        config = json.load(f)

    HOME_DIR = config['home']

    os.makedirs(path.join(HOME_DIR, 'datasets'), exist_ok=True)
    os.makedirs(path.join(HOME_DIR, 'models'), exist_ok=True)


def get_dataset_path(name):
    return path.join(HOME_DIR, 'datasets', name + '.hdf5')


def get_model_path(name):
    return path.join(HOME_DIR, 'models', name + '.hdf5')

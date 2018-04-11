import os
from os import path
import json

import h5py

HOME_DIR = 'home'


def from_config(config_file):
    global HOME_DIR

    if type(config_file) is str:
        with open(config_file) as f:
            config = json.load(f)
    elif type(config_file) is dict:
        config = config_file

    HOME_DIR = config['home']

    os.makedirs(path.join(HOME_DIR, 'datasets'), exist_ok=True)
    os.makedirs(path.join(HOME_DIR, 'models'), exist_ok=True)
    os.makedirs(path.join(HOME_DIR, 'tmp'), exist_ok=True)


def get_dataset_path(name):
    return path.join(HOME_DIR, 'datasets', name + '.hdf5')


def open_dataset(url, *args, prefix=None, raw=False, **kwargs):
    if prefix is None:
        url = get_dataset_path(url)
    if prefix:
        url = path.join(prefix, url)
        url = get_tmp_path(url)

        dir = os.path.dirname(url)
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)

    if raw:
        return open(url, *args, **kwargs)
    else:
        return h5py.File(url, *args, **kwargs)


def get_model_path(name):
    return path.join(HOME_DIR, 'models', name + '.hdf5')


def get_tmp_path(name):
    return path.join(HOME_DIR, 'tmp', name)

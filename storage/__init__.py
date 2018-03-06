import os
from os import path
import json

with open('config/storage_config.json') as f:
    config = json.load(f)

HOME_DIR = config['home']

os.makedirs(path.join(HOME_DIR, 'datasets'), exist_ok=True)


def get_dataset_path(name):
    return path.join(HOME_DIR, 'datasets', name + '.hdf5')


import json

from pymodm import connect
from pymodm import errors

from . import dataset
from . import architecture
from . import model
from . import task

from .dataset import *
from .architecture import *
from .model import *
from .task import *


def from_config(config_path):
    with open(config_path) as f:
        config = json.load(f)

    mongo_url = config['mongo_url']

    connect(mongo_url, alias='metadata')


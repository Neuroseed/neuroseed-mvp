import json

from mongoengine import connect
from mongoengine.errors import *

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

    database = 'metadata'
    connect(database, host=mongo_url, alias='metadata')


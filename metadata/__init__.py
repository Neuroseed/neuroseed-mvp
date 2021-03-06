import json

from mongoengine import connect
from mongoengine.errors import *

from . import dataset
from . import architecture
from . import model
from . import task
from . import errors

from .dataset import *
from .architecture import *
from .model import *
from .task import *


def from_config(config_file):
    if type(config_file) is str:
        with open(config_file) as f:
            config = json.load(f)
    elif type(config_file) is dict:
        config = config_file

    mongo_url = config['mongo_url']

    database = 'metadata'
    connect(database, host=mongo_url, alias='metadata',
            connect=True, socketTimeoutMS=5000, connectTimeoutMS=5000, serverSelectionTimeoutMS=5000,
            heartbeatFrequencyMS=1000)
    # more args:
    # https://api.mongodb.com/python/current/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient

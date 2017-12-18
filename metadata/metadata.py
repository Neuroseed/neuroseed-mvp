import pymongo
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.errors import ConnectionFailure

__all__ = [
    'Metadata'
]


class Metadata:
    def __init__(self, config):
        url = config['mongo_url']
        connect_timeout = config.get('connect_timeout', 3000)
        selection_timeout = config.get('selection_timeout', 3000)

        self.mongo = pymongo.MongoClient(
            url,
            connectTimeoutMS=connect_timeout,
            serverSelectionTimeoutMS=selection_timeout)

    def check_connection(self):
        try:
            # The ismaster command is cheap and does not require auth.
            self.mongo.admin.command('ismaster')
        except ConnectionFailure:
            print("Mongo server not available")

    def get_datasets(self):
        metadata = self.mongo.metadata
        datasets = metadata.datasets

        data = []
        try:
            data = list(datasets.find({}, {'_id': False}))
        except ServerSelectionTimeoutError:
            print('ServerSelectionTimeoutError: Connection refused')

        return data

    def get_models(self):
        metadata = self.mongo.metadata
        models = metadata.models

        data = []
        try:
            data = list(models.find({}, {'_id': False}))
        except ServerSelectionTimeoutError:
            print('ServerSelectionTimeoutError: Connection refused')

        return data

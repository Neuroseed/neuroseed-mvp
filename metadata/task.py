from pymodm import MongoModel, fields

__all__ = [
    'Task'
]

PENDING = 1
RECEIVED = 2
STARTED = 3
SUCCESS = 4
FAILURE = 5
REVOKED = 6
RETRY = 7


class Task(MongoModel):
    id = fields.CharField(primary_key=True)
    status = fields.IntegerField(default=1)
    owner = fields.CharField()
    command = fields.CharField()
    date = fields.TimestampField()
    config_init = lambda: dict()
    config = fields.DictField(default=config_init)

    class Meta:
        connection_alias = 'metadata'
        collection_name = 'tasks'


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
    type = fields.CharField()
    date = fields.TimestampField()
    state = fields.IntegerField(default=PENDING)

    class Meta:
        connection_alias = 'metadata'
        collection_name = 'tasks'


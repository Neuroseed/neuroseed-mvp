from mongoengine import Document
from mongoengine import fields

__all__ = [
    'TaskMetadata'
]

PENDING = 1
RECEIVED = 2
STARTED = 3
SUCCESS = 4
FAILURE = 5
REVOKED = 6
RETRY = 7


class TaskMetadata(Document):
    id = fields.StringField(primary_key=True)
    status = fields.IntField(default=1)
    owner = fields.StringField()
    command = fields.StringField()
    date = fields.LongField()
    config = fields.DictField(default=lambda: dict())

    meta = {
        'allow_inheritance': True,
        'db_alias': 'metadata',
        'collection': 'tasks'
    }

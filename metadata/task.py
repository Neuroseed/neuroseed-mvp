import uuid

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
    id = fields.StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
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

    @classmethod
    def from_id(cls, id):
        return cls.objects.get(id=id)

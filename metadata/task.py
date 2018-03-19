import time
import uuid

from mongoengine import Document
from mongoengine import fields

from .mixin import MetadataMixin

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


class TaskMetadata(Document, MetadataMixin):
    id = fields.StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    status = fields.IntField(default=PENDING)
    owner = fields.StringField(required=True)
    command = fields.StringField(required=True)
    date = fields.LongField(default=lambda: int(time.time()))
    config = fields.DictField(default=lambda: dict())

    meta = {
        'allow_inheritance': True,
        'db_alias': 'metadata',
        'collection': 'tasks'
    }

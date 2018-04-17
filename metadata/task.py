import time
import uuid

from mongoengine import Document
from mongoengine import fields
from mongoengine.queryset.visitor import Q
from mongoengine.errors import DoesNotExist

from .mixin import MetadataMixin

__all__ = [
    'TaskMetadata',
    'get_task',
    'get_tasks'
]

PENDING = 'PENDING'
RECEIVED = 'RECEIVED'
STARTED = 'STARTED'
SUCCESS = 'SUCCESS'
FAILURE = 'FAILURE'
REVOKED = 'REVOKED'
RETRY = 'RETRY'

TASK_STATUS_CODES = [
    PENDING,
    RECEIVED,
    STARTED,
    SUCCESS,
    FAILURE,
    REVOKED,
    RETRY
]

MODEL_TRAIN = 'model.train'
MODEL_TEST = 'model.test'
MODEL_PREDICT = 'model.predict'

TASK_COMMANDS = [
    MODEL_TRAIN,
    MODEL_TEST,
    MODEL_PREDICT
]


class TaskMetadata(Document, MetadataMixin):
    id = fields.StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    status = fields.StringField(default=PENDING, choices=TASK_STATUS_CODES, required=True)
    owner = fields.StringField(required=True)
    command = fields.StringField(choices=TASK_COMMANDS, required=True)
    date = fields.LongField(default=lambda: int(time.time()))
    config = fields.DictField(default=lambda: dict())
    history = fields.DictField()

    meta = {
        'allow_inheritance': True,
        'db_alias': 'metadata',
        'collection': 'tasks'
    }

    def to_dict(self):
        meta = self.to_mongo().to_dict()

        if '_id' in meta:
            meta['id'] = meta['_id']
            del meta['_id']

        del meta['_cls']

        return meta

    def from_dict(self, meta):
        for name in self._fields:
            if name in meta:
                setattr(self, name, meta[name])


def get_task(id, context):
    if not isinstance(id, str):
        raise TypeError('Type of id must be str')

    if not isinstance(context, dict):
        raise TypeError('Type of context must be dict')

    if 'user_id' in context and context['user_id']:
        user_id = context['user_id']
        query = Q(id=id) & Q(owner=user_id)
        meta = TaskMetadata.from_id(query)
    else:
        raise DoesNotExist('task does not exists for None user')

    return meta


def get_tasks(context, filter=None):
    if not isinstance(context, dict):
        raise TypeError('Type of context must be dict')

    if not isinstance(filter, (dict, type(None))):
        raise TypeError('Type of context must be dict')

    if 'user_id' not in context and not context['user_id']:
        raise DoesNotExist('task does not exists for None user')

    user_id = context['user_id']
    query = Q(owner=user_id)
    metas = TaskMetadata.objects(query)

    if filter:
        if 'from' in filter:
            from_ = filter['from']
            metas = metas.skip(from_)

        if 'number' in filter:
            number = filter['number']
            metas = metas.limit(number)

    return metas

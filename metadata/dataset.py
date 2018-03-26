import uuid

from mongoengine import Document, EmbeddedDocument
from mongoengine import fields

from .mixin import MetadataMixin

__all__ = [
    'DatasetMetadata'
]


PENDING = 'PENDING'
RECEIVED = 'RECEIVED'
FAILURE = 'FAILURE'
PUBLISHED = 'PUBLISHED'

DATASET_STATUS_CODES = [
    PENDING,
    RECEIVED,
    FAILURE,
    PUBLISHED
]

CLASSIFICATION = 'CLASSIFICATION'
REGRESSION = 'REGRESSION'

DATASET_CATEGORIES = [
    CLASSIFICATION,
    REGRESSION
]


class DatasetBase(EmbeddedDocument):
    owner = fields.StringField(required=True)
    hash = fields.StringField()
    size = fields.LongField()
    date = fields.LongField()
    title = fields.StringField(required=True)
    description = fields.StringField()
    category = fields.StringField(choices=DATASET_CATEGORIES)
    labels = fields.ListField(fields.StringField())
    shape = fields.ListField(fields.IntField())


class DatasetMetadata(Document, MetadataMixin):
    id = fields.StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    url = fields.StringField()
    status = fields.StringField(default=PENDING, choices=DATASET_STATUS_CODES, required=True)
    is_public = fields.BooleanField(default=False)
    hash = fields.StringField()
    base = fields.EmbeddedDocumentField(DatasetBase, default=lambda: DatasetBase())

    meta = {
        'allow_inheritance': True,
        'db_alias': 'metadata',
        'collection': 'datasets'
    }

import uuid

from mongoengine import Document, EmbeddedDocument
from mongoengine import fields

from .dataset import DatasetMetadata
from .architecture import ArchitectureMetadata
from .mixin import MetadataMixin

__all__ = [
    'ModelMetadata'
]

PENDING = 'PENDING'
INITIALIZE = 'INITIALIZE'
TRAINING = 'TRAINING'
TESTING = 'TESTING'
READY = 'READY'
FAILURE = 'FAILURE'
PUBLISHED = 'PUBLISHED'

MODEL_STATUS_CODES = [
    PENDING,
    INITIALIZE,
    TRAINING,
    TESTING,
    READY,
    FAILURE,
    PUBLISHED
]


class ModelBase(EmbeddedDocument):
    owner = fields.StringField(required=True)
    hash = fields.StringField()
    size = fields.LongField()
    date = fields.LongField()
    title = fields.StringField(required=True)
    description = fields.StringField()
    labels = fields.ListField(field=fields.StringField())
    metrics = fields.DictField(default=lambda: dict())
    architecture = fields.ReferenceField(ArchitectureMetadata, required=True)
    dataset = fields.ReferenceField(DatasetMetadata, required=True)
    # TODO: parent = fields.ReferenceField(Model)
    shape = fields.ListField(field=fields.IntField())

    # category = fields.StringField()

    @property
    def category(self):
        """Return category from dataset"""

        return self.dataset.base.category


class ModelMetadata(Document, MetadataMixin):
    id = fields.StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    url = fields.StringField()
    status = fields.StringField(default=PENDING, choices=MODEL_STATUS_CODES, required=True)
    is_public = fields.BooleanField(default=False)
    hash = fields.StringField()
    base = fields.EmbeddedDocumentField(ModelBase, default=lambda: ModelBase())

    meta = {
        'allow_inheritance': True,
        'db_alias': 'metadata',
        'collection': 'models'
    }

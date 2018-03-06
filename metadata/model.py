from pymodm import EmbeddedMongoModel, MongoModel, fields

from .dataset import Dataset
from .architecture import Architecture

__all__ = [
    'Model'
]

PENDING = 1
INITIALIZE = 2
TRAINING = 3
TESTING = 4
READY = 5


class ModelMetadata(EmbeddedMongoModel):
    owner = fields.CharField()
    hash = fields.CharField()
    size = fields.IntegerField()
    date = fields.TimestampField()
    title = fields.CharField()
    description = fields.CharField()
    category = fields.CharField()
    labels = fields.ListField(field=fields.CharField())
    accuracy = fields.FloatField()
    architecture = fields.ReferenceField(Architecture)
    dataset = fields.ReferenceField(Dataset)
    # TODO: parent = fields.ReferenceField(Model)
    shape = fields.ListField(field=fields.IntegerField())


class Model(MongoModel):
    id = fields.CharField(primary_key=True)
    url = fields.CharField()
    status = fields.IntegerField(default=PENDING)
    is_public = fields.BooleanField(default=False)
    hash = fields.CharField()
    meta_init = lambda: ModelMetadata()
    meta = fields.EmbeddedDocumentField(ModelMetadata, default=meta_init)

    class Meta:
        connection_alias = 'metadata'
        collection_name = 'models'


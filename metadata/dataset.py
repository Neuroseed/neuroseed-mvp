from pymodm import EmbeddedMongoModel, MongoModel, fields

__all__ = [
    'Dataset'
]


PENDING = 1
RECEIVED = 2
FAILURE = 3


class DatasetMetadata(EmbeddedMongoModel):
    owner = fields.CharField()
    hash = fields.CharField()
    size = fields.IntegerField()
    date = fields.TimestampField()
    title = fields.CharField()
    description = fields.CharField()
    category = fields.CharField()
    labels = fields.ListField(field=fields.CharField())
    shape = fields.ListField(field=fields.IntegerField())


class Dataset(MongoModel):
    '''in db mydb.dataset'''
    id = fields.CharField(primary_key=True)
    url = fields.CharField()
    status = fields.IntegerField(default=PENDING)
    is_public = fields.BooleanField(default=False)
    hash = fields.CharField()
    meta_init = lambda: DatasetMetadata()
    meta = fields.EmbeddedDocumentField(DatasetMetadata, default=meta_init)

    class Meta:
        connection_alias = 'metadata'
        collection_name = 'datasets'


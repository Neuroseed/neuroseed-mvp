from mongoengine import Document, EmbeddedDocument
from mongoengine import fields

__all__ = [
    'DatasetMetadata'
]


PENDING = 1
RECEIVED = 2
FAILURE = 3


class DatasetBase(EmbeddedDocument):
    owner = fields.StringField()
    hash = fields.StringField()
    size = fields.LongField()
    date = fields.LongField()
    title = fields.StringField()
    description = fields.StringField()
    category = fields.StringField()
    labels = fields.ListField(fields.StringField())
    shape = fields.ListField(fields.IntField())


class DatasetMetadata(Document):
    '''in db mydb.dataset'''
    id = fields.StringField(primary_key=True)
    url = fields.StringField()
    status = fields.IntField(default=PENDING)
    is_public = fields.BooleanField(default=False)
    hash = fields.StringField()
    base_init = lambda: DatasetBase()
    base = fields.EmbeddedDocumentField(DatasetBase, default=base_init)

    meta = {
        'db_alias': 'metadata',
        'collection': 'datasets'
    }

import uuid

from mongoengine import Document
from mongoengine import fields

__all__ = [
    'ArchitectureMetadata'
]


class ArchitectureMetadata(Document):
    id = fields.StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    is_public = fields.BooleanField(default=False)
    owner = fields.StringField(required=True)
    title = fields.StringField(required=True)
    description = fields.StringField()
    category = fields.StringField()
    architecture = fields.DictField(required=True)

    meta = {
        'allow_inheritance': True,
        'db_alias': 'metadata',
        'collection': 'architectures'
    }

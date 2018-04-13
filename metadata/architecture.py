import uuid

from mongoengine import Document
from mongoengine import fields

from .dataset import DATASET_CATEGORIES
from .mixin import MetadataMixin

__all__ = [
    'ArchitectureMetadata'
]


class ArchitectureMetadata(Document, MetadataMixin):
    id = fields.StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    is_public = fields.BooleanField(default=False)
    owner = fields.StringField(required=True)
    title = fields.StringField(required=True)
    description = fields.StringField()
    category = fields.StringField(choices=DATASET_CATEGORIES)
    architecture = fields.DictField(required=True)

    meta = {
        'allow_inheritance': True,
        'db_alias': 'metadata',
        'collection': 'architectures'
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

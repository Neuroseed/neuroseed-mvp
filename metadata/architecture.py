import uuid

from mongoengine import Document
from mongoengine import fields
from mongoengine.queryset.visitor import Q

from .dataset import DATASET_CATEGORIES
from .mixin import MetadataMixin

__all__ = [
    'ArchitectureMetadata',
    'get_architecture',
    'get_architectures'
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


def get_architecture(id, context):
    if not isinstance(id, str):
        raise TypeError('Type of id must be str')

    if not isinstance(context, dict):
        raise TypeError('Type of context must be dict')

    if 'user_id' in context and context['user_id']:
        user_id = context['user_id']
        query = Q(id=id) & (Q(owner=user_id) | Q(is_public=True))
        meta = ArchitectureMetadata.from_id(query)
    else:
        kwargs = {'id': id, 'is_public': True}
        meta = ArchitectureMetadata.from_id(**kwargs)

    return meta


def get_architectures(context, filter=None):
    if not isinstance(context, dict):
        raise TypeError('Type of context must be dict')

    if not isinstance(filter, (dict, type(None))):
        raise TypeError('Type of context must be dict')

    query = Q(is_public=True)

    if 'user_id' in context and context['user_id']:
        user_id = context['user_id']
        query = query | (Q(is_public=False) & Q(owner=user_id))

    metas = ArchitectureMetadata.objects(query)

    if filter:
        if 'from' in filter:
            from_ = filter['from']
            metas = metas.skip(from_)

        if 'number' in filter:
            number = filter['number']
            metas = metas.limit(number)

    return metas

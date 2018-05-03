import uuid

from mongoengine import Document
from mongoengine import fields
from mongoengine.queryset.visitor import Q

from .dataset import DATASET_CATEGORIES
from .mixin import MetadataMixin
from .errors import ResourcePublishedException

__all__ = [
    'ArchitectureMetadata',
    'get_architecture',
    'get_architectures',
    'update_architecture',
    'delete_architecture'
]

PENDING = 'PENDING'
PUBLISHED = 'PUBLISHED'

ARCHITECTURE_STATUS_CODES = [
    PENDING,
    PUBLISHED
]


class ArchitectureMetadata(Document, MetadataMixin):
    id = fields.StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    is_public = fields.BooleanField(default=False)
    owner = fields.StringField(required=True)
    status = fields.StringField(default=PENDING, choices=ARCHITECTURE_STATUS_CODES, required=True)  # NEW IN V0.5.0
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


def update_architecture(architecture, data, context=None):
    """Delete architecture by id or directly
    Args:
        architecture (str or ArchitectureMetadata): architecture to delete
        data (dict): update fields data
        context (None or dict): context for delete

    Returns:
        None

    Raises:
        TypeError - invalid argument type
        DoesNotExist - architecture does not exist
        KeyError - context not contain user_id key
        ValueError - invalid access rights
    """

    if not isinstance(architecture, (str, ArchitectureMetadata)):
        raise TypeError('type of architecture must be str or ArchitectureMetadata')

    if not isinstance(data, dict):
        raise TypeError('type of data must be dict')

    if not isinstance(context, (dict, type(None))):
        raise TypeError('type of context must be dict or None')

    if isinstance(architecture, str):
        if isinstance(context, type(None)):
            raise ValueError('to access to architecture need user_id')

        user_id = context.get('user_id', None)

        if user_id:
            query = Q(id=architecture) & Q(owner=user_id)
            architecture = ArchitectureMetadata.from_id(query)
        else:
            raise KeyError('context must contain user_id key')

    with architecture.save_context():
        architecture.from_dict(data)


def delete_architecture(architecture, context=None):
    """Delete architecture by id or directly
    Args:
        architecture (str or ArchitectureMetadata): architecture to delete
        context (None or dict): context for delete

    Returns:
        None

    Raises:
        TypeError - invalid argument type
        DoesNotExist - architecture does not exist
        KeyError - context not contain user_id key
        ValueError - invalid access rights
        ResourcePublishedException - can not delete published architecture
    """

    if not isinstance(architecture, (str, ArchitectureMetadata)):
        raise TypeError('Type of architecture must be str or ArchitectureMetadata')

    if not isinstance(context, (dict, type(None))):
        raise TypeError('Type of context must be dict or None')

    if isinstance(architecture, str):
        if isinstance(context, type(None)):
            raise ValueError('to access to architecture need user_id')

        user_id = context.get('user_id', None)

        if user_id:
            query = Q(id=architecture) & Q(owner=user_id)
            architecture = ArchitectureMetadata.from_id(query)
        else:
            raise KeyError('context must contain user_id key')

    if architecture.status == PUBLISHED:
        raise ResourcePublishedException('can not delete published architecture')

    architecture.delete()


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

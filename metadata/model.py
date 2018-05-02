import uuid

from mongoengine import Document, EmbeddedDocument
from mongoengine import fields
from mongoengine.queryset.visitor import Q

from .dataset import DatasetMetadata
from .architecture import ArchitectureMetadata
from .mixin import MetadataMixin
from .errors import ResourcePublishedException

__all__ = [
    'ModelMetadata',
    'get_model',
    'get_models',
    'delete_model'
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

    def __init__(self, *args, **kwargs):
        flatten = None
        if 'flatten' in kwargs:
            flatten = kwargs['flatten']
            del kwargs['flatten']

        super().__init__(*args, **kwargs)

        if flatten:
            self.from_flatten(flatten)

        self.url = self.id

    def flatten(self):
        """Return model in flatten representation"""

        meta = self.to_mongo().to_dict()

        if '_id' in meta:
            meta['id'] = meta['_id']
            del meta['_id']

        meta.update(meta['base'])
        del meta['base']
        del meta['_cls']

        return meta

    to_dict = flatten

    def from_flatten(self, meta):
        """Restore model metadata from flatten representation"""

        for name in self._fields:
            if not name is 'base' and name in meta:
                setattr(self, name, meta[name])

        for name in self.base._fields:
            if name in meta:
                setattr(self.base, name, meta[name])

    from_dict = from_flatten


def get_model(id, context):
    if not isinstance(id, str):
        raise TypeError('Type of id must be str')

    if not isinstance(context, dict):
        raise TypeError('Type of context must be dict')

    if 'user_id' in context and context['user_id']:
        user_id = context['user_id']
        query = Q(id=id) & (Q(base__owner=user_id) | Q(is_public=True))
        meta = ModelMetadata.from_id(query)
    else:
        kwargs = {'id': id, 'is_public': True}
        meta = ModelMetadata.from_id(**kwargs)

    return meta


def delete_model(model, context=None):
    """Delete model by id or directly
    Args:
        model (str or ModelMetadata): model to delete
        context (None or dict): context for delete

    Returns:
        None

    Raises:
        TypeError - invalid argument type
        DoesNotExist - model does not exist
        KeyError - context not contain user_id key
        ValueError - invalid access rights
        ResourcePublishedException - can not delete published model
    """

    if not isinstance(model, (str, ModelMetadata)):
        raise TypeError('Type of model must be str or ModelMetadata')

    if not isinstance(context, (dict, type(None))):
        raise TypeError('Type of context must be dict or None')

    if isinstance(model, str):
        if isinstance(context, type(None)):
            raise ValueError('to access to model need user_id')

        user_id = context.get('user_id', None)

        if user_id:
            query = Q(id=model) & Q(base__owner=user_id)
            model = ModelMetadata.from_id(query)
        else:
            raise KeyError('context must contain user_id key')

    if model.status == PUBLISHED:
        raise ResourcePublishedException('can not delete published model')

    model.delete()


def get_models(context, filter=None):
    if not isinstance(context, dict):
        raise TypeError('Type of context must be dict')

    if not isinstance(filter, (dict, type(None))):
        raise TypeError('Type of context must be dict')

    query = Q(is_public=True)

    if 'user_id' in context and context['user_id']:
        user_id = context['user_id']
        query = query | (Q(is_public=False) & Q(base__owner=user_id))

    metas = ModelMetadata.objects(query)

    if filter:
        if 'from' in filter:
            from_ = filter['from']
            metas = metas.skip(from_)

        if 'number' in filter:
            number = filter['number']
            metas = metas.limit(number)

    return metas

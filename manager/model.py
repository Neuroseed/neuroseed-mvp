import uuid

import metadata
from . import utils
from webapi import errors


def get_model_meta(id):
    try:
        model = metadata.ModelMetadata(id=id)
    except metadata.DoesNotExist:
        model = None

    if model:
        meta = {
            'id': model.id,
            'is_public': model.is_public,
            'hash': model.hash,
            'owner': model.base.owner,
            'size': model.base.size,
            'date': model.base.date,
            'title': model.base.title,
            'description': model.base.description,
            'category': model.base.category,
            'labels': model.base.labels,
            'accuracy': model.base.accuracy,
            'dataset': model.base.dataset
        }
        return meta
    else:
        raise metadata.DoesNotExist('Model metadata does not exist')


def create_model_meta(meta):
    # request to document mapping
    base = meta.copy()
    del base['is_public']
    document = {
        'is_public': meta['is_public'],
        'base': base
    }

    # save model metadata to database
    model = metadata.ModelMetadata(**document)
    id = str(uuid.uuid4())
    model.id = id
    model.url = id
    model.base.owner = '0'
    model.save()

    return id


def get_models():
    models_meta = metadata.ModelMetadata.objects.all()
    ids = [meta.id for meta in models_meta]

    return ids


def create_model_task(command, config, model_id):
    try:
        model = metadata.ModelMetadata.objects(id=model_id)
    except metadata.DoesNotExist as err:
        raise errors.ModelDoesNotExist from err

    config["model"] = model_id

    id = utils.create_task(command, config)

    return id


def train_model(config, model_id):
    return create_model_task('model.train', config, model_id)


def test_model(config, model_id):
    return create_model_task('model.test', config, model_id)


def predict_model(config, model_id):
    return create_model_task('model.predict', config, model_id)

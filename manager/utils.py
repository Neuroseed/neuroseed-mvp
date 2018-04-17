import json
import functools
import logging

import celery

import metadata

logger = logging.getLogger(__name__)

app = celery.Celery('tasks')

EMBEDDED_WORKER = False


def from_config(config):
    global EMBEDDED_WORKER

    if isinstance(config, str):
        with open(config) as f:
            config = json.load(f)
    elif isinstance(config, dict):
        config = config
    else:
        raise TypeError('Type of config must be str or dict')

    EMBEDDED_WORKER = config.get('embedded_worker', EMBEDDED_WORKER)

    if not EMBEDDED_WORKER:
        celery_config = config.get('celery_config', None)
        if celery_config:
            app.config_from_object(celery_config)
        else:
            raise KeyError('manager need celery config to initialize')


def prepare_metadata(metadata_cls, metadata):
    if isinstance(metadata, str):
        metadata = metadata_cls.from_id(id=metadata)
    elif isinstance(metadata, metadata_cls):
        pass
    else:
        type_ = type(metadata)
        msg = 'type of metadata must be str or {metatype}, not {type}'.format(metatype=metadata_cls, type=type_)
        raise TypeError(msg)

    return metadata

prepare_dataset = functools.partial(prepare_metadata, metadata.DatasetMetadata)
prepare_architecture = functools.partial(prepare_metadata, metadata.ArchitectureMetadata)
prepare_model = functools.partial(prepare_metadata, metadata.ModelMetadata)
prepare_task = functools.partial(prepare_metadata, metadata.TaskMetadata)

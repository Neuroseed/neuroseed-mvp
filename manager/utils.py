import json
import functools
import logging

import celery

import metadata

logger = logging.getLogger(__name__)

app = celery.Celery('tasks')


def from_config(config_file):
    if type(config_file) is str:
        with open(config_file) as f:
            config = json.load(f)
    elif type(config_file) is dict:
        config = config_file

    app.config_from_object(config)


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

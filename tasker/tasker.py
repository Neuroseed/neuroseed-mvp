import uuid
import celery
from celery.result import AsyncResult

import metadata
from .app import app
from webapi import errors


def start_task(name, *args, task_id=None, **kwargs):
    return app.send_task(
        name, 
        args=args, 
        kwargs=kwargs, 
        task_id=task_id)


def get_task(task_id):
    return AsyncResult(task_id)


def wait_task(task_id):
    task = AsyncResult(task_id)
    return task.get(timeout=10)


def create_task(command, config, id=None, start=True):
    if not type(command) is str:
        raise TypeError('command type must be str')

    if not type(config) is dict:
        raise TypeError('config type must be dict')

    id = id or str(uuid.uuid4())

    task = metadata.TaskMetadata()
    task.id = id
    task.command = command
    task.config = config
    task.save()

    if start:
        start_task(command, task_id=id)

    return id


def create_model_task(command, config, model_id):
    try:
        model = metadata.ModelMetadata.objects(id=model_id)
    except metadata.DoesNotExist as err:
        raise errors.ModelDoesNotExist from err

    config["model"] = model_id

    id = create_task(command, config)

    return id


def train_model(config, model_id):
    return create_model_task('model.train', config, model_id)


def test_model(config, model_id):
    return create_model_task('model.test', config, model_id)


def predict_model(config, model_id):
    return create_model_task('model.predict', config, model_id)

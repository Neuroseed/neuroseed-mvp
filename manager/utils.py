import json
import uuid
import logging

import celery
from celery.result import AsyncResult

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


def start_task(name, *args, task_id=None, **kwargs):
    task = app.send_task(
        name,
        args=args,
        kwargs=kwargs,
        task_id=task_id)

    logger.debug('Send task {id} to worker'.format(id=task_id))

    return task


def get_task(task_id):
    return AsyncResult(task_id)


def wait_task(task_id):
    task = AsyncResult(task_id)
    return task.get(timeout=10)


def create_task(command, config, owner, id=None, start=True):
    if not type(command) is str:
        raise TypeError('command type must be str')

    if not type(config) is dict:
        raise TypeError('config type must be dict')

    id = id or str(uuid.uuid4())

    task = metadata.TaskMetadata()
    task.id = id
    task.owner = owner
    task.command = command
    task.config = config
    task.save()

    if start:
        start_task(command, task_id=id)

    return id

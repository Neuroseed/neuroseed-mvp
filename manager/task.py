import uuid
import logging

from celery.result import AsyncResult
from celery.task import control
import gevent

from metadata.task import TaskMetadata
import metadata
from . import utils
from .utils import app

logger = logging.getLogger(__name__)

CELERY_CONNECTION_TIMEOUT = 5


class Task:
    def __init__(self):
        self.metadata = TaskMetadata()


def terminate(task):
    task = utils.prepare_task(task)

    control.revoke(task.id, terminate=True)
    task.delete()


def start_task(task, *args, **kwargs):
    task = utils.prepare_task(task)

    with gevent.Timeout(CELERY_CONNECTION_TIMEOUT):
        task = app.send_task(
            task.command,
            args=args,
            kwargs=kwargs,
            task_id=task.id)

    logger.debug('Send task {id} to worker'.format(id=task.id))

    return task


def get_task(task_id):
    return AsyncResult(task_id)


def wait_task(task_id):
    task = AsyncResult(task_id)
    return task.get(timeout=10)


def create_task(command, config, context, start=True):
    if not type(command) is str:
        raise TypeError('command type must be str')

    if not type(config) is dict:
        raise TypeError('config type must be dict')

    if 'user_id' in context:
        user_id = context['user_id']
    else:
        raise KeyError('To create task need context user_id')

    with metadata.TaskMetadata().save_context() as task:
        task.id = str(uuid.uuid4())
        task.owner = user_id
        task.command = command
        task.config = config

    if start:
        try:
            start_task(task)
        except gevent.timeout.Timeout:
            with task.save_context():
                task.state = metadata.task.FAILURE
                task.history['error'] = 'Can not send task'

            raise RuntimeError('Can not send task')

    return task

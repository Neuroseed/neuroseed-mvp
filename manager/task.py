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


def start_embedded_task(task, *args, **kwargs):
    import threading

    def _target():
        import worker
        worker.start_task(task)

    t = threading.Thread(target=_target)
    t.daemon = True
    t.start()


def celery_send_task(task, *args, **kwargs):
    try:
        with gevent.Timeout(CELERY_CONNECTION_TIMEOUT):
            task = app.send_task(
                task.command,
                args=args,
                kwargs=kwargs,
                task_id=task.id)
    except gevent.timeout.Timeout:
        raise RuntimeError('Can not send task')


def start_task(task, *args, **kwargs):
    task = utils.prepare_task(task)

    if utils.EMBEDDED_WORKER:
        start_embedded_task(task, *args, **kwargs)
    else:
        celery_send_task(task, *args, **kwargs)

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

    task = metadata.TaskMetadata()

    task.id = str(uuid.uuid4())
    task.owner = user_id
    task.command = command
    task.config = config

    if start:
        start_task(task)

    task.save()

    return task

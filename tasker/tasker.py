import uuid
import celery
from celery.result import AsyncResult

import metadata
from .app import app


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


def train_model(model_id, config):
    try:
        model = metadata.Model.objects.get({'_id': model_id})
    except metadata.errors.DoesNotExist as err:
        raise ValueError() from err

    config["model"] = model_id
    task = {
        "command": "train",
        "config": config
    }

    # TODO: replace by one function
    task_id = uuid.uuid4().hex

    task = metadata.Task.from_document(task)
    task.id = task_id
    task.save()

    start_task('model.train', task_id=task_id)

    return task_id


def test_model():
    return start_task('model.test')


def predict_model():
    return start_task('model.predict')

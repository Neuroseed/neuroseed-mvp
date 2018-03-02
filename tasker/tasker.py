import celery
from .app import app


def start_task(name, *args):
    task = app.send_task(name, args=args)
    return task.get(timeout=10)


def train_model(id):
    return start_task('train_model', id)


def test_model(id):
    return start_task('test_model', id)


def predict_model(id):
    return start_task('predict_model', id)

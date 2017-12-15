import celery
from .app import app


@app.task
def get_datasets():
    return {'datasets': []}


@app.task
def get_models():
    return {'models': []}


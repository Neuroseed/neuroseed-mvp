import celery
from .app import app


@app.task(name='train_model')
def train_model(id):
    return {'id': id}

@app.task(name='test_model')
def test_model(id):
    return {'id': id}

@app.task(name='predict_model')
def predict_model(id):
    return {'id': id}


from .train_model import *


@app.task(bind=True, name='model.test')
def test_model(self):
    task_id = self.request.id
    return {'id': task_id}


@app.task(bind=True, name='model.predict')
def predict_model(self):
    task_id = self.request.id
    return {'id': task_id}

import traceback

from celery import states

import metadata
import storage
from ..app import app
from . import base


def predict_model(model, x):

    result = model.predict(x, verbose=1)

    print('Predict done!')

    return result


def predict_on_task_exc(task):
    if type(task) is str:
        task = metadata.TaskMetadata.from_id(id=task)

    config = task.config

    dataset_id = config['dataset']
    dataset_meta = metadata.DatasetMetadata.from_id(id=dataset_id)

    model_id = config['model']
    model_meta = metadata.ModelMetadata.from_id(id=model_id)

    dataset = base.prepare_dataset(dataset_meta)
    print('Dataset loaded')

    (x, _), _ = base.slice_dataset(dataset, 1.0)
    print('Dataset sliced')

    model = base.prepare_model(model_meta)
    print('Model loaded')

    result = predict_model(model, x)

    # save result
    tmp_name = task.id

    with storage.open_dataset(tmp_name, mode='w', prefix='tmp') as h5:
        h5.create_dataset('y', data=result)

    with task.save_context():
        task.history['result'] = tmp_name


def predict_on_task(task):
    if type(task) is str:
        task = metadata.TaskMetadata.from_id(id=task)

    with task.save_context():
        task.status = metadata.task.STARTED

    try:
        predict_on_task_exc(task)

        with task.save_context():
            task.status = metadata.task.SUCCESS
    except Exception as ex:
        with task.save_context():
            task.status = metadata.task.FAILURE
            task.history['error'] = {
                'type': type(ex).__name__,
                'error': str(ex),
                'traceback': traceback.format_exc()
            }

        raise


@app.task(bind=True, name='model.predict')
def celery_predict_model(self):
    task_id = self.request.id

    try:
        predict_on_task(task_id)
    except Exception:
        self.update_state(state=states.FAILURE)

        raise

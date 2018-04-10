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


def predict_on_task(task):
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
    tmp_id = task.id
    tmp_name = tmp_id + '.hdf5'

    with storage.open_dataset(tmp_name, mode='w', prefix='tmp') as h5:
        h5.create_dataset('y', data=result)

    with task.save_context():
        task.history['result'] = tmp_id


@app.task(bind=True, name='model.predict')
def init_predict_model(self):
    task_id = self.request.id
    task = metadata.TaskMetadata.from_id(id=task_id)

    try:
        predict_on_task(task)
    except Exception as ex:
        self.update_state(state=states.STARTED)

        with task.save_context():
            task.history['error'] = {
                'type': type(ex).__name__,
                'error': str(ex),
                'traceback': traceback.format_exc()
            }

        raise

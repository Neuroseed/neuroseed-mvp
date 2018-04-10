import traceback
import collections

from celery import states

import metadata
from ..app import app
from . import base


def test_model(model, x, y):
    # ETA = Estimated Time of Arrival
    result = model.evaluate(x, y, verbose=1)

    print('Evaluate done!')

    if isinstance(result, collections.Iterable):
        metrics = {metric: value for value, metric in zip(result, model.metrics_names)}
    else:
        metrics = {
            'loss': result
        }

    return metrics


def test_on_task(task):
    config = task.config

    dataset_id = config['dataset']
    dataset_meta = metadata.DatasetMetadata.from_id(id=dataset_id)

    model_id = config['model']
    model_meta = metadata.ModelMetadata.from_id(id=model_id)

    dataset = base.prepare_dataset(dataset_meta)
    print('Dataset loaded')

    (x, y), (_, _) = base.slice_dataset(dataset, 1.0)
    print('Dataset sliced')

    model = base.prepare_model(model_meta)
    print('Model loaded')

    metrics = test_model(model, x, y)

    # save result
    with task.save_context():
        task.history['metrics'] = metrics


@app.task(bind=True, name='model.test')
def init_test_model(self):
    task_id = self.request.id
    task = metadata.TaskMetadata.from_id(id=task_id)

    try:
        test_on_task(task)
    except Exception as ex:
        self.update_state(state=states.STARTED)

        with task.save_context():
            task.history['error'] = {
                'type': type(ex).__name__,
                'error': str(ex),
                'traceback': traceback.format_exc()
            }

        raise
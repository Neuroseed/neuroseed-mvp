import traceback
import collections

from keras.models import save_model as keras_save_models
from celery import states

import metadata
import storage
from ..app import app
from .. import constructor
from .history_callback import HistoryCallback
from . import base

DATASET_SLICE_FACTOR = 0.8


def create_model(architecture, shape):
    model = constructor.create_model(architecture, shape)
    model.summary()

    return model


def get_final_metrics(model, x_test, y_test):
    print('Evaluate...')

    result = model.evaluate(x_test, y_test, verbose=1)

    print('Evaluate done!')

    if isinstance(result, collections.Iterable):
        metrics = {metric: value for value, metric in zip(result, model.metrics_names)}
    else:
        metrics = {
            'loss': result
        }

    print('Metrics:', metrics)

    return metrics


def train_model(model, x_train, y_train, x_test, y_test, config, callbacks):
    constructor.compile_model(model, config)

    batch_size = config.get('batch_size', 32)
    epochs = config.get('epochs', 1)

    model.fit(
        x_train,
        y_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_data=(x_test, y_test),
        shuffle="batch",
        callbacks=callbacks)

    metrics = get_final_metrics(model, x_test, y_test)

    print('Train done!')

    return metrics


def save_model(model, meta=None, path=None):
    if meta:
        model_name = meta.url
        path = storage.get_model_path(model_name)

    keras_save_models(model, path)


def train_on_model(model_meta, config, callbacks=[]):
    dataset_meta = model_meta.base.dataset

    architecture_meta = model_meta.base.architecture
    architecture = architecture_meta.architecture

    dataset = base.prepare_dataset(dataset_meta)
    print('Dataset loaded')

    (x_train, y_train), (x_test, y_test) = base.slice_dataset(dataset, DATASET_SLICE_FACTOR)
    print('Dataset sliced')

    shape = x_train.shape[1:]

    model = create_model(architecture, shape)

    if model_meta:
        with model_meta.save_context():
            model_meta.status = metadata.model.TRAINING

    metrics = train_model(model, x_train, y_train, x_test, y_test, config, callbacks)

    print('model meta: {}'.format(model_meta))
    save_model(model, model_meta)

    # save model metrics
    if model_meta:
        with model_meta.save_context():
            model_meta.status = metadata.model.READY
            model_meta.base.metrics = metrics

    return metrics


def train_on_task_exc(task):
    if type(task) is str:
        task = metadata.TaskMetadata.from_id(id=task)

    model_id = task.config['model']
    model_meta = metadata.ModelMetadata.from_id(id=model_id)

    config = task.config

    dataset_meta = model_meta.base.dataset
    dataset = base.prepare_dataset(dataset_meta)
    (x_train, _), _ = base.slice_dataset(dataset, DATASET_SLICE_FACTOR)

    batch_size = config.get('batch_size', 32)
    epochs = config.get('epochs', 1)
    examples = x_train.shape[0]
    train_examples_number = examples
    batch_in_epoch = train_examples_number // batch_size + 1

    h = HistoryCallback(task, epochs, batch_in_epoch, examples)
    callbacks = [h]

    return train_on_model(model_meta, config, callbacks)


def train_on_task(task):
    if type(task) is str:
        task = metadata.TaskMetadata.from_id(id=task)

    try:
        train_on_task_exc(task)

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


@app.task(bind=True, name='model.train')
def celery_train_model(self):
    task_id = self.request.id

    try:
        train_on_task(task_id)
    except Exception:
        self.update_state(state=states.STARTED)

        raise

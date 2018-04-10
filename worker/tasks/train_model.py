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


def train(architecture=None, dataset_meta=None, config=None, task=None):
    model_meta = None

    if task:
        model_id = task.config['model']
        model_meta = metadata.ModelMetadata.from_id(id=model_id)

        dataset_meta = model_meta.base.dataset

        architecture_meta = model_meta.base.architecture
        architecture = architecture_meta.architecture

        config = task.config

    if not config:
        config = {}

    dataset = base.prepare_dataset(dataset_meta)
    print('Dataset loaded')

    (x_train, y_train), (x_test, y_test) = base.slice_dataset(dataset, 0.8)
    print('Dataset sliced')

    batch_size = config.get('batch_size', 32)
    epochs = config.get('epochs', 1)
    train_examples_number = x_train.shape[0]
    batch_in_epoch = train_examples_number // batch_size + 1

    callbacks = []
    if task:
        h = HistoryCallback(task, epochs, batch_in_epoch)
        callbacks.append(h)

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


@app.task(bind=True, name='model.train')
def init_train_model(self):
    task_id = self.request.id
    task = metadata.TaskMetadata.from_id(id=task_id)

    try:
        train(task=task)
    except Exception as ex:
        self.update_state(state=states.STARTED)

        with task.save_context():
            task.history['error'] = {
                'type': type(ex).__name__,
                'error': str(ex),
                'traceback': traceback.format_exc()
            }

        raise

import collections

from keras.models import save_model
import h5py

import metadata
import storage
from ..app import app
from .. import constructor
from .history_callback import HistoryCallback
from . import base


class TrainModelCommand(base.BaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dataset_meta = None
        self.architecture_meta = None
        self.model_meta = None

    def train_model_from_meta(self):
        task_id = self.request.id

        self.task_meta = self.get_task(task_id)

        model_id = self.task_meta.config['model']
        self.model_meta = self.get_model(model_id)

        self.dataset_meta = self.model_meta.base.dataset

        self.architecture_meta = self.model_meta.base.architecture

        # state started
        self.update_state_started()

        config = self.task_meta.config
        architecture = self.architecture_meta.architecture

        (x_train, y_train), (x_test, y_test) = self.get_dataset(self.dataset_meta)

        batch_size = config.get('batch_size', 32)
        epochs = config.get('epochs', 1)
        train_examples_number = x_train.shape[0]
        batch_in_epoch = train_examples_number // batch_size + 1

        h = HistoryCallback(self.task_meta, epochs, batch_in_epoch)
        callbacks = [h]

        shape = x_train.shape[1:]

        model = self.create_model(architecture, shape)
        metrics = self.train_model(model, x_train, y_train, x_test, y_test, config, callbacks)

        self.save_model(model, self.model_meta)

        # save model metrics
        with self.model_meta.save_context():
            self.model_meta.base.metrics = metrics

        # state success
        self.update_state_success()

    def update_state_started(self):
        super().update_state_success()

        with self.model_meta.save_context():
            self.model_meta.status = metadata.model.TRAINING

        print('Start train task: {}'.format(self.task_meta.id))

    def update_state_success(self):
        super().update_state_success()

        with self.model_meta.save_context():
            self.model_meta.status = metadata.model.READY

        print('End train task: {}'.format(self.task_meta.id))

    def open_dataset(self, file_name, *args, mode='r', **kwargs):
        return h5py.File(file_name, *args, mode=mode, **kwargs)

    def slice_dataset(self, dataset, div_factor=0.8):
        # get dataset shape
        x = dataset['x']
        y = dataset['y']
        examples = x.shape[0]

        # get train/test subsets
        border = int(examples * div_factor)
        x_train = x[border:]
        y_train = y[border:]
        x_test = x[:border]
        y_test = y[:border]

        return (x_train, y_train), (x_test, y_test)

    def get_dataset(self, dataset_meta):
        dataset_name = dataset_meta.url
        dataset_path = storage.get_dataset_path(dataset_name)

        print('Open dataset:', dataset_path)
        dataset = self.open_dataset(dataset_path)

        return self.slice_dataset(dataset)

    def save_model(self, model, model_meta):
        # save model
        model_name = model_meta.url
        model_path = storage.get_model_path(model_name)
        save_model(model, model_path)

    def get_final_metrics(self, model, x_test, y_test):
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

    def create_model(self, architecture, shape):
        model = constructor.create_model(architecture, shape)
        model.summary()

        return model

    def train_model(self, model, x_train, y_train, x_test, y_test, config, callbacks):
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

        metrics = self.get_final_metrics(model, x_test, y_test)

        print('Train done!')

        return metrics


@app.task(bind=True, base=TrainModelCommand, name='model.train')
def init_train_model(self):
    return self.train_model_from_meta()

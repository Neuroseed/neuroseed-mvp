import time

import celery
from celery import states
from keras import callbacks
from keras.models import save_model
import h5py

import metadata
import storage
from ..app import app
from .. import constructor


class HistoryCallback(callbacks.Callback):
    UPDATE_ON_BATCH = 10

    def __init__(self, task, epochs, batch_in_epoch):
        super().__init__()

        self._task = task
        self.batch_in_epoch = batch_in_epoch

        task.history['batch'] = {}
        task.history['epoch'] = {}

        task.history['epochs'] = epochs
        task.history['current_epoch'] = 0

        task.history['batches'] = batch_in_epoch * epochs
        task.history['current_batch'] = 0
        task.save()

    @property
    def task(self):
        return self._task

    def on_batch_end(self, batch, logs=None):
        del logs['batch']  # delete batch number
        del logs['size']  # delete batch size
        logs['time'] = round(time.time(), 3)  # add current time

        batch_history = self.task.history['batch']

        for key in logs:
            history = batch_history.setdefault(key, [])
            value = float(logs[key])
            history.append(value)

        current_epoch = self.task.history['current_epoch']
        batch = (current_epoch - 1) * self.batch_in_epoch + batch
        self.task.history['current_batch'] = batch

        if batch % self.UPDATE_ON_BATCH == 0:
            self.task.save()

    def on_epoch_begin(self, epoch, logs=None):
        self.task.history['current_epoch'] = epoch + 1

        self.task.save()

    def on_epoch_end(self, epoch, logs=None):
        logs['time'] = round(time.time(), 3)  # add current time

        epoch_history = self.task.history['epoch']

        for key in logs:
            history = epoch_history.setdefault(key, [])
            value = float(logs[key])
            history.append(value)

        self.task.history['current_epoch'] = epoch + 1

        self.task.save()

    def on_train_end(self, logs=None):
        pass


class TrainModelCommand(celery.Task):
    def get_dataset(self, dataset_id):
        try:
            dataset_meta = metadata.DatasetMetadata.from_id(id=dataset_id)
        except metadata.DoesNotExist:
            print('dataset does not exist')
            self.update_state(state=states.FAILURE)
            raise

        return dataset_meta

    def get_architecture(self, architecture_id):
        try:
            architecture_meta = metadata.ArchitectureMetadata.from_id(id=architecture_id)
        except metadata.DoesNotExist:
            print('architecture does not exist')
            self.update_state(state=states.FAILURE)
            raise

        return architecture_meta

    def get_model(self, model_id):
        try:
            model_meta = metadata.ModelMetadata.from_id(id=model_id)
        except metadata.DoesNotExist:
            self.update_state(state=states.FAILURE)
            raise

        return model_meta

    def get_task(self, task_id):
        try:
            task_meta = metadata.TaskMetadata.from_id(id=task_id)
        except metadata.DoesNotExist:
            self.update_state(state=states.FAILURE)
            raise

        return task_meta

    def update_state_started(self, task_meta, model_meta):
        self.update_state(state=states.STARTED)

        task_meta.status = metadata.task.STARTED
        task_meta.save()

        model_meta.status = metadata.model.TRAINING
        model_meta.save()

        print('Start train task: {}'.format(task_meta.id))

    def update_state_success(self, task_meta, model_meta):
        self.update_state(state=states.SUCCESS)

        task_meta.status = metadata.task.SUCCESS
        task_meta.save()

        model_meta.status = metadata.model.READY
        model_meta.save()

        print('End train task: {}'.format(task_meta.id))

    def slice_dataset(self, dataset_meta):

        # load dataset
        dataset_name = dataset_meta.url
        dataset_path = storage.get_dataset_path(dataset_name)
        print('Open dataset:', dataset_path)
        dataset = h5py.File(dataset_path, 'r')

        # get dataset shape
        x = dataset['x']
        y = dataset['y']
        examples = x.shape[0]

        # get train/test subsets
        div_factor = 0.8
        border = int(examples * div_factor)
        x_train = x[border:]
        y_train = y[border:]
        x_test = x[:border]
        y_test = y[:border]

        return (x_train, y_train), (x_test, y_test)

    def save_model(self, model, model_meta):
        # save model
        model_name = model_meta.url
        model_path = storage.get_model_path(model_name)
        save_model(model, model_path)

    def train_model(self, dataset_meta, architecture_meta, model_meta, task_meta):
        config = task_meta.config

        (x_train, y_train), (x_test, y_test) = self.slice_dataset(dataset_meta)

        # create keras model
        architecture = architecture_meta.architecture
        train_examples_number = x_train.shape[0]
        shape = x_train.shape[1:]
        print('Input shape:', shape)
        model = constructor.create_model(architecture, shape)
        model.summary()

        constructor.compile_model(model, config)

        # train
        batch_size = config.get('batch_size', 32)
        epochs = config.get('epochs', 1)

        batch_in_epoch = train_examples_number // batch_size + 1

        h = HistoryCallback(task_meta, epochs, batch_in_epoch)
        callbacks = [h]

        # train keras model
        model.fit(
            x_train,
            y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_data=(x_test, y_test),
            shuffle="batch",
            callbacks=callbacks)

        self.save_model(model, model_meta)


@app.task(bind=True, base=TrainModelCommand, name='model.train')
def init_train_model(self):
    task_id = self.request.id

    task_meta = self.get_task(task_id)

    model_id = task_meta.config['model']
    model_meta = self.get_model(model_id)

    dataset_meta = model_meta.base.dataset

    architecture_meta = model_meta.base.architecture

    # state started
    self.update_state_started(task_meta, model_meta)

    self.train_model(dataset_meta, architecture_meta, model_meta, task_meta)

    # state success
    self.update_state_success(task_meta, model_meta)

    return {}

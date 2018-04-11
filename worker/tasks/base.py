import celery
from celery import states
import h5py
import keras
from keras.models import load_model

import metadata
import storage


class BaseTask(celery.Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.task_meta = None

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

    def update_state_started(self):
        self.update_state(state=states.STARTED)

        with self.task_meta.save_context():
            self.task_meta.status = metadata.task.STARTED

    def update_state_success(self,):
        self.update_state(state=states.SUCCESS)

        with self.task_meta.save_context():
            self.task_meta.status = metadata.task.SUCCESS


def prepare_dataset(dataset):
    if isinstance(dataset, str):
        meta = metadata.DatasetMetadata.from_id(id=dataset)
        dataset = storage.open_dataset(meta.url)
    elif isinstance(dataset, metadata.DatasetMetadata):
        dataset = storage.open_dataset(dataset.url)
    elif isinstance(dataset, h5py.File):
        pass
    else:
        type_ = type(dataset)
        msg = 'dataset type must be str or metadata.DatasetMetadata or h5py.File, not {type}'.format(type=type_)
        raise TypeError(msg)

    return dataset


def prepare_model(model):
    if isinstance(model, str):
        meta = metadata.ModelMetadata.from_id(id=model)
        model_path = storage.get_model_path(meta.url)
        model = load_model(model_path)
    elif isinstance(model, metadata.ModelMetadata):
        model_path = storage.get_model_path(model.url)
        model = load_model(model_path)
    elif isinstance(model, keras.Model):
        pass
    else:
        type_ = type(model)
        msg = 'model type must be str or metadata.ModelMetadata or keras.Model, not {type}'.format(type=type_)
        raise TypeError(msg)

    return model


def slice_dataset(dataset, slice):
    if not isinstance(slice, float):
        raise ValueError('type of slice must be float')

    dataset = prepare_dataset(dataset)

    def slice_part(part):
        shape = dataset[part].shape
        len = shape[0]
        border = int(len * slice)

        a_train = dataset[part][:border]
        a_test = dataset[part][border:]

        return a_train, a_test

    if 'x' in dataset:
        x = slice_part('x')
    else:
        raise ValueError('dataset must contain x attribute')

    if 'y' in dataset:
        y = slice_part('y')
    else:
        y = (None, None)
        print('Warning: dataset not contain y attribute')

    return list(zip(x, y))

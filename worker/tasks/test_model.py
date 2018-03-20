import uuid

import celery
from celery import states
from keras.models import load_model
import h5py

import metadata
import storage
from ..app import app
from .. import constructor


class TestModelCommand(celery.Task):
    def get_dataset(self, dataset_id):
        try:
            dataset_meta = metadata.DatasetMetadata.from_id(dataset_id)
        except metadata.DoesNotExist:
            print('dataset does not exist')
            self.update_state(state=states.FAILURE)
            raise

        return dataset_meta

    def get_architecture(self, architecture_id):
        try:
            architecture_meta = metadata.ArchitectureMetadata.from_id(architecture_id)
        except metadata.DoesNotExist:
            print('architecture does not exist')
            self.update_state(state=states.FAILURE)
            raise

        return architecture_meta

    def get_model(self, model_id):
        try:
            model_meta = metadata.ModelMetadata.from_id(model_id)
        except metadata.DoesNotExist:
            self.update_state(state=states.FAILURE)
            raise

        return model_meta

    def get_task(self, task_id):
        try:
            task_meta = metadata.TaskMetadata.from_id(task_id)
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

    def test_model(self, dataset_meta, model_meta, task_meta):
        config = task_meta.config

        # load dataset
        dataset_name = dataset_meta.url
        dataset_path = storage.get_dataset_path(dataset_name)
        print('Open dataset:', dataset_path)
        dataset = h5py.File(dataset_path, 'r')

        # get dataset shape
        shape = dataset['x'].shape[1:]
        print('Input shape:', shape)

        # get x dataset
        x = dataset['x']
        y = dataset['y']

        # load model
        model_name = model_meta['url']
        model_path = storage.get_model_path(model_name)
        model = load_model(model_path)

        result = model.evaluate(x, y, verbose=0)

        # save result
        task_meta.config['result'] = result
        task_meta.save()


@app.task(bind=True, base=TestModelCommand, name='model.test')
def init_test_model(self):
    task_id = self.request.id

    task_meta = self.get_task(task_id)

    dataset_id = task_meta.config['dataset']
    dataset_meta = self.get_dataset(dataset_id)

    model_id = task_meta.config['model']
    model_meta = self.get_model(model_id)

    # state started
    self.update_state_started(task_meta, model_meta)

    self.test_model(dataset_meta, model_meta, task_meta)

    # state success
    self.update_state_success(task_meta, model_meta)

    return {}

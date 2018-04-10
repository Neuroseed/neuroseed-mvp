import uuid

import celery
from celery import states
from keras.models import load_model
import h5py

import metadata
import storage
from ..app import app
from . import base


class PreditctModelCommand(base.BaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dataset_meta = None
        self.architecture_meta = None
        self.model_meta = None

    def predict_from_meta(self):
        task_id = self.request.id

        self.task_meta = self.get_task(task_id)
        config = self.task_meta.config

        dataset_id = config['dataset']
        self.dataset_meta = self.get_dataset(dataset_id)

        model_id = config['model']
        self.model_meta = self.get_model(model_id)

        # state started
        self.update_state_started()

        dataset = base.prepare_dataset(self.dataset_meta)
        print('Dataset loaded')

        (x, _), _ = base.slice_dataset(dataset, 1.0)
        print('Dataset sliced')

        model = base.prepare_model(self.model_meta)
        print('Model loaded')

        result = self.predict_model(x, model)

        # save result
        tmp_id = self.task_meta.id
        tmp_name = tmp_id + '.hdf5'

        with storage.open_dataset(tmp_name, mode='w', prefix='tmp') as h5:
            h5.create_dataset('y', data=result)

        with self.task_meta.save_context():
            self.task_meta.history['result'] = tmp_id

        # state success
        self.update_state_success()

    def predict_model(self, x, model):

        result = model.predict(x, verbose=1)

        print('Predict done!')

        return result


@app.task(bind=True, base=PreditctModelCommand, name='model.predict')
def init_predict_model(self):
    self.predict_from_meta()

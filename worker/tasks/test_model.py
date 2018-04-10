import collections

import metadata
from ..app import app
from . import base


class TestModelCommand(base.BaseTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.dataset_meta = None
        self.architecture_meta = None
        self.model_meta = None

    def update_state_started(self):
        super().update_state_success()

        with self.model_meta.save_context():
            self.model_meta.status = metadata.model.TESTING

        print('Start test task: {}'.format(self.task_meta.id))

    def update_state_success(self):
        super().update_state_success()

        with self.model_meta.save_context():
            self.model_meta.status = metadata.model.READY

        print('End test task: {}'.format(self.task_meta.id))

    def test_from_meta(self):
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

        (x, y), (_, _) = base.slice_dataset(dataset, 1.0)
        print('Dataset sliced')

        model = base.prepare_model(self.model_meta)
        print('Model loaded')

        metrics = self.test_model(x, y, model)

        # save result
        with self.task_meta.save_context():
            self.task_meta.history['metrics'] = metrics

        # state success
        self.update_state_success()

    def test_model(self, x, y, model):
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


@app.task(bind=True, base=TestModelCommand, name='model.test')
def init_test_model(self):
    self.test_from_meta()

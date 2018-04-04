import celery
from celery import states

import metadata


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

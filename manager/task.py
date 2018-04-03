import uuid

import metadata
from metadata import TaskMetadata
from celery.app import control


def terminate(task_id):
    control.terminate(task_id)
    metadata.TaskMetadata.from_id(id=task_id).delete()

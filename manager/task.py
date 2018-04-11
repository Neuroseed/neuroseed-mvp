import metadata
from celery.task import control


def terminate(task_id):
    control.revoke(task_id, terminate=True)
    metadata.TaskMetadata.from_id(id=task_id).delete()

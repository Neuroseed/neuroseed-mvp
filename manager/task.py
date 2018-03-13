import uuid

import metadata


def get_task(self, req, resp, id):
    try:
        task = metadata.TaskMetadata.objects(id=id)
    except metadata.DoesNotExist as err:
        raise metadata.DoesNotExist('Task does not exists') from err

    meta = {
        'id': id,
        'command': task.command,
        'config': task.configs
    }
    return meta


def create_task(meta):
    task = metadata.TaskMetadata(**meta)
    task.id = str(uuid.uuid4())
    task.save()

    return task.id


def get_tasks():
    tasks = metadata.TaskMetadata.objects.all()
    ids = [task.id for task in tasks]

    return ids

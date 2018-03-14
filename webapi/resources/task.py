import uuid
import falcon
from falcon.media.validators import jsonschema

import metadata
from ..schema.task import TASK_SCHEMA

__all__ = [
    'TaskResource'
]


class TaskResource:
    def on_get(self, req, resp, id):
        try:
            task = metadata.TaskMetadata.objects(id=id)
        except metadata.DoesNotExist:
            task = None

        if task:
            resp.status = falcon.HTTP_200
            resp.media = {
                'id': id,
                'command': task.command,
                'config': task.configs
            }
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Task does not exists'
            }

    @jsonschema.validate(TASK_SCHEMA)
    def on_post(self, req, resp):
        user_id = req.context['user']
        print('User ID:', user_id)

        task = metadata.TaskMetadata(**req.media)
        task.id = str(uuid.uuid4())
        task.owner = user_id
        task.save()

        resp.status = falcon.HTTP_200
        resp.media = {
            'id': task.id
        }


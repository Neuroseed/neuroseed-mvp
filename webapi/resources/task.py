import uuid
import falcon
from falcon.media.validators import jsonschema

import metadata
from .schema import TASK_SCHEMA

__all__ = [
    'TaskResource'
]


class TaskResource:
    def on_get(self, req, resp, id=None):
        try:
            task = metadata.Task.objects.get({'_id': id})
        except metadata.Task.DoesNotExist:
            task = None

        if task:
            resp.media = {
                'success': True,
                'model': task.to_son()
            }
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                'success': False,
                'error': 'Task does not exist'
            }

    @jsonschema.validate(TASK_SCHEMA)
    def on_post(self, req, resp):
        task = metadata.Task.from_document(req.media)
        task.id = uuid.uuid4()
        task.save()

        resp.media = {
            'success': True,
            'model': task.id
        }


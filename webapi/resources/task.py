import uuid
import logging

import falcon
from falcon.media.validators import jsonschema

import metadata
from ..schema.task import TASK_SCHEMA

__all__ = [
    'TaskResource'
]

logger = logging.getLogger(__name__)


class TaskResource:
    def on_get(self, req, resp, id):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            task = metadata.TaskMetadata.objects(id=id)
        except metadata.DoesNotExist:
            logger.debug('Task {id} does not exist'.format(id=id))
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
        logger.debug('Authorize user {id}'.format(id=user_id))

        task = metadata.TaskMetadata(**req.media)
        task.id = str(uuid.uuid4())
        task.owner = user_id
        task.save()

        logger.debug('User {uid} create model {did}'.format(uid=user_id, did=task.id))

        resp.status = falcon.HTTP_200
        resp.media = {
            'id': task.id
        }


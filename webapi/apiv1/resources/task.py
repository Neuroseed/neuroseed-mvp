import uuid
import logging

import falcon
from falcon.media.validators import jsonschema

import metadata
import manager
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
            context = {'user_id': user_id}
            task = metadata.get_task(id, context)
        except metadata.DoesNotExist:
            logger.debug('Task {id} does not exist'.format(id=id))
            task = None

        if task:
            resp.status = falcon.HTTP_200
            task_dict = task.to_dict()
            result_keys = ['id', 'status', 'command', 'date', 'config']
            resp.media = {key: task_dict[key] for key in result_keys if key in task_dict}
        else:
            raise falcon.HTTPNotFound(
                title="Task not found",
                description="Task metadata does not exist"
            )

    @jsonschema.validate(TASK_SCHEMA)
    def on_post(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        with metadata.TaskMetadata().save_context() as task:
            task.from_dict(req.media)
            task.id = str(uuid.uuid4())
            task.owner = user_id

        logger.debug('User {uid} create model {did}'.format(uid=user_id, did=task.id))

        resp.status = falcon.HTTP_200
        resp.media = {
            'id': task.id
        }

    def on_delete(self, req, resp, id):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            context = {'user_id': user_id}
            task = metadata.get_task(id, context)
        except metadata.DoesNotExist:
            logger.debug('Task {id} does not exist'.format(id=id))

            raise falcon.HTTPNotFound(
                title="Task not found",
                description="Task metadata does not exist"
            )

        manager.terminate(id)
        task.delete()

        resp.status = falcon.HTTP_200
        resp.media = {}

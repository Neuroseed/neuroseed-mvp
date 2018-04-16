import logging

import falcon
from falcon.media.validators import jsonschema

import metadata
from ...schema.model_test import MODEL_TEST_SCHEMA
import manager
from .... import errors

__all__ = [
    'ModelTestResource',
    'ModelTestStatusResource',
    'ModelTestResult'
]

logger = logging.getLogger(__name__)


class ModelTestResource:
    @jsonschema.validate(MODEL_TEST_SCHEMA)
    def on_post(self, req, resp, id):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            config = req.media
            context = {'user_id': 'user_id'}
            task = manager.test_model(id, config, context)
            task_id = task.id
        except (errors.ModelDoesNotExist, metadata.DoesNotExist):
            raise falcon.HTTPNotFound(
                title="Model not found",
                description="Model metadata does not exist"
            )
        except RuntimeError:
            raise falcon.HTTPInternalServerError(
                title="Can not create task",
                description="Can not create task. Internal connection error. Task is deleted."
            )

        logger.debug('User {uid} create task {tid}'.format(uid=user_id, tid=task_id))

        resp.status = falcon.HTTP_200
        resp.media = {
            'id': task_id,
        }


class ModelTestStatusResource:
    def on_get(self, req, resp, tid):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            task = metadata.TaskMetadata.from_id(id=tid, owner=user_id)
        except metadata.DoesNotExist:
            logger.debug('Task {id} does not exist'.format(id=id))

            raise falcon.HTTPNotFound(
                title="Task not found",
                description="Task metadata does not exist"
            )

        resp.status = falcon.HTTP_200
        resp.media = {
            'id': tid,
            'config': task.config
        }


class ModelTestResult:
    def on_get(self, req, resp, tid):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            task = metadata.TaskMetadata.from_id(id=tid, owner=user_id)
        except metadata.DoesNotExist:
            logger.debug('Task {id} does not exist'.format(id=id))

            raise falcon.HTTPNotFound(
                title="Task not found",
                description="Task metadata does not exist"
            )

        if 'metrics' not in task.config:
            raise falcon.HTTPNotFound(
                title="Task is not completed",
                description="Task is not completed"
            )

        resp.status = falcon.HTTP_200
        resp.media = task.config['metrics']

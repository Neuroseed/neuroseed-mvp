import logging

import falcon
from falcon.media.validators import jsonschema

import metadata
import manager
from ...schema.model_train import MODEL_TRAIN_SCHEMA
from .... import errors

__all__ = [
    'ModelTrainResource',
    'ModelTrainStatusResource',
    'ModelTrainResult'
]

logger = logging.getLogger(__name__)


class ModelTrainResource:
    @jsonschema.validate(MODEL_TRAIN_SCHEMA)
    def on_post(self, req, resp, id):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        config = req.media

        try:
            task_id = manager.train_model(config, id, user_id)
        except errors.ModelDoesNotExist:
            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Model does not exists'
            }
            return

        logger.debug('User {uid} create task {did}'.format(uid=user_id, did=id))

        resp.status = falcon.HTTP_200
        resp.media = {
            'id': task_id,
        }


class ModelTrainStatusResource:
    def on_get(self, req, resp, tid):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            task = metadata.TaskMetadata.from_id(tid, owner=user_id)
        except metadata.DoesNotExist:
            logger.debug('Task {id} does not exist'.format(id=id))

            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Task does not exists'
            }
            return

        resp.status = falcon.HTTP_200
        resp.media = {
            'id': tid,
            'config': task.config
        }


class ModelTrainResult:
    def on_get(self, req, resp, tid):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            task = metadata.TaskMetadata.from_id(tid, owner=user_id)
        except metadata.DoesNotExist:
            logger.debug('Task {id} does not exist'.format(id=id))

            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Task does not exists'
            }
            return

        if 'history' not in task.config:
            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Task is not completed'
            }
            return

        resp.status = falcon.HTTP_200
        resp.media = task.config['history']

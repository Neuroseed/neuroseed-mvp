import logging

import falcon
from falcon.media.validators import jsonschema

import metadata
from ...schema.model_predict import MODEL_PREDICT_SCHEMA
import manager
from ... import errors

__all__ = [
    'ModelPredictResource',
    'ModelPredictStatusResource',
    'ModelPredictResult'
]

logger = logging.getLogger(__name__)


class ModelPredictResource:
    @jsonschema.validate(MODEL_PREDICT_SCHEMA)
    def on_post(self, req, resp, mid):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        config = req.media

        try:
            task_id = manager.predict_model(config, mid, user_id)
        except errors.ModelDoesNotExist:
            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Model does not exists'
            }
            return

        logger.debug('User {uid} create task {tid}'.format(uid=user_id, tid=task_id))

        resp.status = falcon.HTTP_200
        resp.media = {
            'task': task_id,
        }


class ModelPredictStatusResource:
    def on_get(self, req, resp, tid):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            task = metadata.TaskMetadata.from_id(tid)
        except metadata.DoesNotExist:
            logger.debug('Task {id} does not exist'.format(id=id))
            task = None

        if task:
            resp.status = falcon.HTTP_200
            resp.media = {
                'id': id,
                'config': task.configs
            }
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Task does not exists'
            }


class ModelPredictResult:
    def on_get(self, req, resp, tid):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            task = metadata.TaskMetadata.from_id(tid)
        except metadata.DoesNotExist:
            logger.debug('Task {id} does not exist'.format(id=id))
            task = None

        if task:
            resp.status = falcon.HTTP_200
            resp.media = {
                'result': task.config['result']
            }
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Task does not exists'
            }

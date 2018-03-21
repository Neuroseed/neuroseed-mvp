import logging

import falcon
from falcon.media.validators import jsonschema

import metadata
import storage
from ...schema.model_predict import MODEL_PREDICT_SCHEMA
import manager
from .... import errors

__all__ = [
    'ModelPredictResource',
    'ModelPredictStatusResource',
    'ModelPredictResult'
]

logger = logging.getLogger(__name__)


class ModelPredictResource:
    @jsonschema.validate(MODEL_PREDICT_SCHEMA)
    def on_post(self, req, resp, id):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        config = req.media

        try:
            task_id = manager.predict_model(config, id, user_id)
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


class ModelPredictResult:
    def on_get(self, req, resp, tid):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            task = metadata.TaskMetadata.from_id(tid)
        except metadata.DoesNotExist:
            logger.debug('Task {id} does not exist'.format(id=id))

            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Task does not exists'
            }
            return

        if 'result' not in task.config:
            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Task is not completed'
            }
            return

        temp_id = task.config['result']
        temp_path = storage.get_tmp_path(temp_id)

        # TODO: send by multipart stream
        with open(temp_path) as f:
            raw = f.read()
            resp.stream.write(raw)

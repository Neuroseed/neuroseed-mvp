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

        try:
            config = req.media
            context = {'user_id': 'user_id'}
            task = manager.predict_model(id, config, context)
            task_id = task.id
        except errors.ModelDoesNotExist:
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


class ModelPredictStatusResource:
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


class ModelPredictResult:
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

        if 'result' not in task.config:
            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Task is not completed'
            }
            return

        temp_id = task.config['result']
        temp_path = storage.get_tmp_path(temp_id)

        resp.status = falcon.HTTP_200

        # TODO: send by multipart stream
        with open(temp_path) as f:
            raw = f.read()
            resp.stream.write(raw)

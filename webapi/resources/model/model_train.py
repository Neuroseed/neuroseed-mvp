import logging

import falcon
from falcon.media.validators import jsonschema

from ...schema.model_train import MODEL_TRAIN_SCHEMA
import manager
from ... import errors

__all__ = [
    'ModelTrainResource'
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
            'id': id,
            'task': task_id,
        }

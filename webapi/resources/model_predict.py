import logging

import falcon
from falcon.media.validators import jsonschema

from ..schema.model_predict import MODEL_PREDICT_SCHEMA
import manager
from .. import errors

__all__ = [
    'ModelPredictResource'
]

logger = logging.getLogger(__name__)


class ModelPredictResource:
    @jsonschema.validate(MODEL_PREDICT_SCHEMA)
    def on_post(self, req, resp, mid, did):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        config = {
            'dataset': did
        }

        try:
            task_id = manager.predict_model(config, mid, user_id)
        except errors.ModelDoesNotExist:
            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Model does not exists'
            }
            return

        logger.debug('User {uid} create task {did}'.format(uid=user_id, did=did))

        resp.status = falcon.HTTP_200
        resp.media = {
            'task': task_id,
        }

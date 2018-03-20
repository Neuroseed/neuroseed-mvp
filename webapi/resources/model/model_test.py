import logging

import falcon
from falcon.media.validators import jsonschema

import metadata
from ...schema.model_test import MODEL_TEST_SCHEMA
import manager
from ... import errors

__all__ = [
    'ModelTestResource',
]

logger = logging.getLogger(__name__)


class ModelTestResource:
    @jsonschema.validate(MODEL_TEST_SCHEMA)
    def on_post(self, req, resp, id):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        config = req.media

        try:
            task_id = manager.test_model(config, id, user_id)
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

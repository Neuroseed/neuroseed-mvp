import uuid
import falcon
from falcon.media.validators import jsonschema

import metadata
from .schema import MODEL_TRAIN_SCHEMA
import tasker

__all__ = [
    'ModelTrainResource'
]


class ModelTrainResource:
    @jsonschema.validate(MODEL_TRAIN_SCHEMA)
    def on_post(self, req, resp, id):
        config = req.media

        try:
            task_id = tasker.train_model(id, config)
        except ValueError:
            resp.status = falcon.HTTP_404
            return

        resp.media = {
            'success': True,
            'task': task_id,
        }


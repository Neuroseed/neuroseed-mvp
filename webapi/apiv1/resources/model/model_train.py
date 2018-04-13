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

        try:
            model = metadata.ModelMetadata.from_id(id=id, base__owner=user_id)
        except metadata.DoesNotExist:
            logger.debug('Model {id} does not exist'.format(id=id))

            raise falcon.HTTPNotFound(
                title="Model not found",
                description="Model metadata does not exist"
            )

        if model.status != metadata.model.PENDING:
            raise falcon.HTTPError(
                code=falcon.HTTP_304,
                title="Already Trained",
                description="Model already trained"
            )

        model.status = metadata.model.INITIALIZE
        model.save()

        try:
            task_id = manager.train_model(req.media, id, user_id)
        except errors.ModelDoesNotExist:
            raise falcon.HTTPNotFound(
                title="Model not found",
                description="Model metadata does not exist"
            )

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
            'config': task.config,
            'history': task.history
        }


class ModelTrainResult:
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

        if task.status in (metadata.task.SUCCESS, metadata.task.FAILURE):
            resp.status = falcon.HTTP_201
        else:
            resp.status = falcon.HTTP_200
        resp.media = task.history

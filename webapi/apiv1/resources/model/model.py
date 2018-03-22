import uuid
import logging

import falcon
from falcon.media.validators import jsonschema

import metadata
from ...schema.model import MODEL_SCHEMA

__all__ = [
    'ModelResource'
]

logger = logging.getLogger(__name__)


class ModelResource:
    auth = {
        'optional_methods': ['GET']
    }

    def on_get(self, req, resp, id=None):
        if id:
            self.get_model_meta(req, resp, id)
        else:
            self.get_description(req, resp)

    def get_model_meta(self, req, resp, id):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            if user_id:
                kwargs = {'id': id, 'base__owner': user_id}
            else:
                kwargs = {'id': id, 'is_public': True}

            model_meta = metadata.ModelMetadata.from_id(**kwargs)
        except metadata.DoesNotExist:
            logger.debug('Model {id} does not exist'.format(id=id))

            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Model metadata does not exist'
            }
            return

        resp.status = falcon.HTTP_200
        resp.media = {
            'id': model_meta.id,
            'is_public': model_meta.is_public,
            'hash': model_meta.hash,
            'owner': model_meta.base.owner,
            'size': model_meta.base.size,
            'date': model_meta.base.date,
            'title': model_meta.base.title,
            'description': model_meta.base.description,
            'category': model_meta.base.category,
            'labels': model_meta.base.labels,
            'accuracy': model_meta.base.accuracy,
            'dataset': model_meta.base.dataset
        }

    def get_description(self, req, resp):
        resp.status = falcon.HTTP_404
        resp.media = {
            'error': 'Model metadata does not exist'
        }

    def on_post(self, req, resp, id=None):
        if id:
            self.update_model_meta(req, resp, id)
        else:
            self.create_model_meta(req, resp)

    def update_model_meta(self, req, resp, id):
        resp.status = falcon.HTTP_400
        resp.media = {
            'error': 'Can not update model metadata'
        }
        return

    @jsonschema.validate(MODEL_SCHEMA)
    def create_model_meta(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        # request to document mapping
        base = req.media.copy()
        del base['is_public']
        document = {
            'is_public': req.media['is_public'],
            'base': base
        }

        # save model metadata to database
        model_meta = metadata.ModelMetadata(**document)
        model_meta.id = str(uuid.uuid4())
        model_meta.url = model_meta.id
        model_meta.base.owner = user_id
        model_meta.save()

        logger.debug('User {uid} create model {did}'.format(uid=user_id, did=model_meta.id))

        resp.status = falcon.HTTP_200
        resp.media = {
            'id': model_meta.id
        }

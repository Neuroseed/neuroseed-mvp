import base64
import logging

import falcon
import uuid
from falcon.media.validators import jsonschema
import metadata
import storage
from ..schema.dataset import DATASET_SCHEMA

__all__ = [
    'DatasetResource'
]

logger = logging.getLogger(__name__)


class DatasetResource:
    def on_get(self, req, resp, id=None):
        if id:
            self.get_dataset_meta(req, resp, id)
        else:
            self.get_description(req, resp)

    def get_dataset_meta(self, req, resp, id):
        try:
            dataset_meta = metadata.DatasetMetadata.objects(id=id)
        except metadata.DoesNotExist:
            logger.debug('Dataset {id} does not exist'.format(id=id))
            dataset_meta = None

        if dataset_meta:
            resp.status = falcon.HTTP_200
            resp.media = {
                'id': dataset_meta.id,
                'is_public':dataset_meta.is_public,
                'title': dataset_meta.meta.title,
                'description': dataset_meta.meta.description,
                'category':dataset_meta.meta.category,
                'labels':dataset_meta.meta.labels
            }
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Dataset metadata doesnt exist'
            }
    
    def get_description(self, req, resp):
        resp.media = {
            'id':id
        }

    def on_post(self, req, resp, id=None):
        if id:
            self.upload_dataset(req, resp, id)
        else:
            self.create_dataset_meta(req, resp)

    def save_dataset(self, req, resp, dataset_meta):
        url = dataset_meta.url
        file_path = storage.get_dataset_path(url)

        with open(file_path, 'wb') as f:
            data = base64.b64decode(req.media)
            f.write(data)

        dataset_meta.status = metadata.dataset.RECEIVED
        dataset_meta.save()

        logger.debug('Dataset {id} received'.format(id=dataset_meta.id))
        resp.media = {'id': dataset_meta.id}

    def dataset_already_uploaded(self, req, resp, id):
        logger.debug('Dataset {id} alerady uploaded'.format(id=id))
        resp.status = falcon.HTTP_405
        resp.media = {
            'error': 'Dataset already uploaded'
        }

    def upload_dataset(self, req, resp):
        try:
            dataset_meta = metadata.DatasetMetadata.objects(id=id)
        except metadata.DoesNotExist:
            dataset_meta = None

        if dataset_meta:
            if dataset_meta.status == metadata.dataset.PENDING:
                self.save_dataset(req, resp, dataset_meta)
            elif dataset_meta.status == metadata.dataset.RECEIVED:
                self.dataset_already_uploaded(req, resp, id)
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Dataset metadata does not exist'
            }

    @jsonschema.validate(DATASET_SCHEMA)
    def create_dataset_meta(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        base = req.media.copy()
        del base['is_public']
        document = {
            'is_public': req.media['is_public'],
            'base': base
        }
        dataset_meta = metadata.DatasetMetadata(**document)
        dataset_meta.id = str(uuid.uuid4())
        dataset_meta.url = dataset_meta.id
        dataset_meta.base.owner = user_id
        dataset_meta.save()

        logger.debug('User {uid} create dataset {did}'.format(uid=user_id, did=dataset_meta.id))

        resp.status = falcon.HTTP_200
        resp.media = {
            'id': dataset_meta.id
        }

import logging
import uuid
import base64
import cgi

from mongoengine.queryset.visitor import Q
import falcon
from falcon.media.validators import jsonschema

import metadata
import storage
from ..schema.dataset import DATASET_SCHEMA

__all__ = [
    'DatasetResource'
]

logger = logging.getLogger(__name__)

MAX_DATASET_SIZE = 1 * 10**9  # in bytes


class DatasetResource:
    auth = {
        'optional_methods': ['GET']
    }

    def on_get(self, req, resp, id=None):
        if id:
            self.get_dataset_meta(req, resp, id)
        else:
            self.get_description(req, resp)

    def get_dataset_meta(self, req, resp, id):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            if user_id:
                query = Q(id=id) & (Q(base__owner=user_id) | Q(is_public=True))
                dataset_meta = metadata.DatasetMetadata.from_id(query)
            else:
                kwargs = {'id': id, 'is_public': True}
                dataset_meta = metadata.DatasetMetadata.from_id(**kwargs)
        except metadata.DoesNotExist:
            logger.debug('Dataset {id} does not exist'.format(id=id))
            dataset_meta = None

        if dataset_meta:
            resp.status = falcon.HTTP_200
            resp.media = {
                'id': dataset_meta.id,
                'is_public': dataset_meta.is_public,
                'title': dataset_meta.base.title,
                'description': dataset_meta.base.description,
                'category': dataset_meta.base.category,
                'labels': dataset_meta.base.labels
            }
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Dataset metadata does not exist'
            }
    
    def get_description(self, req, resp):
        resp.status = falcon.HTTP_404
        resp.media = {
            'error': 'Dataset metadata does not exist'
        }

    def on_post(self, req, resp, id=None):
        if id:
            self.upload_dataset(req, resp, id)
        else:
            self.create_dataset_meta(req, resp)

    def save_dataset_v1(self, req, resp, dataset_meta):
        """
        Plain text base64 encoding dataset upload
        """

        url = dataset_meta.url
        file_path = storage.get_dataset_path(url)

        with open(file_path, 'wb') as f:
            data = base64.b64decode(req.media)
            f.write(data)

        dataset_meta.status = metadata.dataset.RECEIVED
        dataset_meta.save()

        logger.debug('Dataset {id} received'.format(id=dataset_meta.id))
        resp.media = {'id': dataset_meta.id}

    def save_dataset_v2(self, req, resp, dataset_meta):
        """
        Multipart dataset upload        
        """
        print('Content type:', req.content_type)
        print('Content length:', req.content_length)

        if req.content_length > MAX_DATASET_SIZE:
            resp.status = falcon.HTTP_413
            resp.media = {
                'error': 'Dataset is too large'
            }
            return

        CHUNK_SIZE_BYTES = 4096
        env = req.env
        env.setdefault('QUERY_STRING', '')

        form = cgi.FieldStorage(fp=req.stream, environ=env)

        file_item = form['file']
        if file_item.file:
            url = dataset_meta.url
            file_path = storage.get_dataset_path(url)

            with open(file_path, 'wb') as f:
                logger.debug('Save dataset to file {path}'.format(path=file_path))

                while True:
                    chunk = file_item.file.read(CHUNK_SIZE_BYTES)
                    if not chunk:
                        break
                    f.write(chunk)
        else:
            logger.debug('No file item')

        resp.status = falcon.HTTP_200
        resp.media = {'id': dataset_meta.id}

    def dataset_already_uploaded(self, req, resp, id):
        logger.debug('Dataset {id} alerady uploaded'.format(id=id))
        resp.status = falcon.HTTP_405
        resp.media = {
            'error': 'Dataset already uploaded'
        }

    def upload_dataset(self, req, resp, id):
        try:
            dataset_meta = metadata.DatasetMetadata.from_id(id=id)
        except metadata.DoesNotExist:
            dataset_meta = None

        if dataset_meta:
            if dataset_meta.status == metadata.dataset.PENDING:
                upload_version = 2

                if upload_version == 1:
                    self.save_dataset_v1(req, resp, dataset_meta)
                elif upload_version == 2:
                    self.save_dataset_v2(req, resp, dataset_meta)

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
        document = {
            'base': base
        }
        if 'is_public' in base:
            del base['is_public']
            document['is_public'] = req.media['is_public']

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

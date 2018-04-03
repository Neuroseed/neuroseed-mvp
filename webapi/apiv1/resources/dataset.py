import os
import logging
import hashlib
import uuid
import base64
import cgi

from mongoengine.queryset.visitor import Q
import falcon
from falcon.media.validators import jsonschema
import h5py

import metadata
import storage
from ..schema.dataset import DATASET_SCHEMA

__all__ = [
    'DatasetResource'
]

logger = logging.getLogger(__name__)

MAX_DATASET_SIZE = 1 * 10**9  # in bytes


def file_to_hash(file_path):
    hash = hashlib.sha256()

    with open(file_path, 'rb') as f:
        while True:
            raw = f.read(1024)

            if not raw:
                break

            hash.update(raw)

    return hash.hexdigest()


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

            raise falcon.HTTPNotFound(
                title="Dataset not found",
                description="Dataset metadata does not exist"
            )

        resp.status = falcon.HTTP_200
        dataset_meta_dict = dataset_meta.to_dict()
        result_keys = ['id', 'status', 'is_public', 'title', 'description', 'category', 'labels']
        resp.media = {key: dataset_meta_dict[key] for key in result_keys if key in dataset_meta_dict}
    
    def get_description(self, req, resp):
        raise falcon.HTTPNotFound(
            title="Dataset not found",
            description="Dataset metadata does not exist"
        )

    def on_post(self, req, resp, id=None):
        if id:
            self.upload_dataset(req, resp, id)
        else:
            self.create_dataset_meta(req, resp)

    def save_dataset(self, req, resp, dataset_meta):
        """
        Multipart dataset upload        
        """
        print('Content type:', req.content_type)
        print('Content length:', req.content_length)

        if req.content_length > MAX_DATASET_SIZE:
            raise falcon.HTTPRequestEntityTooLarge(
                title="Dataset is too large",
                description="Dataset size must be less than {size} bytes".format(size=MAX_DATASET_SIZE)
            )

        CHUNK_SIZE_BYTES = 4096
        env = req.env
        env.setdefault('QUERY_STRING', '')

        form = cgi.FieldStorage(fp=req.stream, environ=env)

        file_item = form['file']
        if file_item.file:
            url = dataset_meta.url
            file_path = storage.get_dataset_path(url)

            # save dataset
            with open(file_path, 'wb') as f:
                logger.debug('Save dataset to file {path}'.format(path=file_path))

                while True:
                    chunk = file_item.file.read(CHUNK_SIZE_BYTES)
                    if not chunk:
                        break
                    f.write(chunk)

            # validate hdf5
            try:
                with h5py.File(file_path, 'r') as f:
                    _ = f['x']
                    _ = f['y']
            except OSError as err:
                os.remove(file_path)

                raise falcon.HTTPUnsupportedMediaType(
                    description="Can not open dataset. Invalid type."
                )
            except KeyError as err:
                os.remove(file_path)

                raise falcon.HTTPUnsupportedMediaType(
                    description="Dataset has not 'x' or 'y' keys"
                )

            # save dataset size
            statinfo = os.stat(file_path)
            file_size = statinfo.st_size
            dataset_meta.base.size = int(file_size)

            # save dataset hash
            dataset_meta.base.hash = file_to_hash(file_path)

            # change status
            dataset_meta.status = metadata.dataset.RECEIVED
            dataset_meta.save()
        else:
            logger.debug('Multipart not contain file item')

            raise falcon.HTTPUnsupportedMediaType(
                description="Multipart must contain 'file' field"
            )

        resp.status = falcon.HTTP_200
        resp.media = {'id': dataset_meta.id}

    def dataset_already_uploaded(self, req, resp, id):
        logger.debug('Dataset {id} alerady uploaded'.format(id=id))

        raise falcon.HTTPMethodNotAllowed(
            title="Method Not Allowed",
            description="Dataset already uploaded")

    def upload_dataset(self, req, resp, id):
        try:
            dataset_meta = metadata.DatasetMetadata.from_id(id=id)
        except metadata.DoesNotExist:
            dataset_meta = None

        if dataset_meta:
            if dataset_meta.status == metadata.dataset.PENDING:
                self.save_dataset(req, resp, dataset_meta)

            elif dataset_meta.status == metadata.dataset.RECEIVED:
                self.dataset_already_uploaded(req, resp, id)
        else:
            raise falcon.HTTPNotFound(
                title="Dataset not found",
                description="Dataset metadata does not exist"
            )

    @jsonschema.validate(DATASET_SCHEMA)
    def create_dataset_meta(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        with metadata.DatasetMetadata().save_context() as dataset_meta:
            dataset_meta.from_flatten(req.media)
            dataset_meta.id = str(uuid.uuid4())
            dataset_meta.url = dataset_meta.id
            dataset_meta.base.owner = user_id

        logger.debug('User {uid} create dataset {did}'.format(uid=user_id, did=dataset_meta.id))

        resp.status = falcon.HTTP_200
        resp.media = {
            'id': dataset_meta.id
        }

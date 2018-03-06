import base64

import falcon
from falcon.media.validators import jsonschema

import metadata
import storage
from .schema import schema

__all__ = [
    'DatasetResource'
]

class DatasetResource:
    def on_get(self, req, resp, id=None):
        if id:
            self.get_dataset_meta(req, resp, id)
        else:
            self.get_description(req, resp)

    def get_dataset_meta(self, req, resp, id):
        resp.media = {
            'success': True,
            'id': id
        }

    def get_description(self, req, resp):
        resp.media = {
            'success': True,
            'description': 'text'
        }

    def on_post(self, req, resp, id=None):
        if id:
            self.upload_dataset(req, resp, id)
        elif id:
            self.create_dataset_meta(req, resp, id)
        else:
            self.init_dataset(req, resp)

    def save_dataset(self, req, resp, dataset_meta):
        url = dataset_meta.url
        file_path = storage.get_dataset_path(url)

        with open(file_path, 'wb') as f:
            data = base64.b64decode(req.media)
            f.write(data)

        dataset_meta.status = metadata.dataset.RECEIVED
        dataset_meta.save()

        resp.media = {'success': True}

    def dataset_already_uploaded(self, req, resp):
        resp.status = falcon.HTTP_405
        resp.media = {
            'success': False,
            'error': 'Dataset already uploaded'
        }

    def upload_dataset(self, req, resp, id):
        try:
            dataset_meta = metadata.Dataset.objects.get({'_id': str(id)})
        except metadata.Dataset.DoesNotExist:
            dataset_meta = None

        if dataset_meta:
            if dataset_meta.status == metadata.dataset.PENDING:
                self.save_dataset(req, resp, dataset_meta)
            elif dataset_meta.status == metadata.dataset.RECEIVED:
                self.dataset_already_uploaded(req, resp)
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                'success': False,
                'error': 'Dataset metadata does not exist'
            }

    def init_dataset(self, req, resp):
        pass

    @jsonschema.validate(schema)
    def create_dataset_meta(self, req, resp):
        resp.media = {
            'success': True,
        }


import base64
import falcon
import uuid
from falcon.media.validators import jsonschema
import metadata
import storage
from .schema import DATASET_SCHEMA

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
        try:
            dataset_meta = metadata.DatasetMetadata.objects(id=id)
        except metadata.DoesNotExist:
            dataset_meta = None

        if dataset_meta:
            resp.media = {
                'success': True,
                'dataset': dataset_meta.to_son()
            }
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                'success': False,
                'error': 'Dataset metadata doesnt exist'
            }
    
    def get_description(self, req, resp):
        resp.media = {
            'success': True,
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

        resp.media = {'success': True}

    def dataset_already_uploaded(self, req, resp):
        resp.status = falcon.HTTP_405
        resp.media = {
            'success': False,
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
                self.dataset_already_uploaded(req, resp)
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                'success': False,
                'error': 'Dataset metadata does not exist'
            }

    @jsonschema.validate(DATASET_SCHEMA)
    def create_dataset_meta(self, req, resp):
        dataset_meta = metadata.DatasetMetadata(**req.media)
        dataset_meta.id = uuid.uuid4().hex
        dataset_meta.url = dataset_meta.id
        dataset_meta.save()
        print(dataset_meta.id)
        resp.media = {
            'success': True,
            'dataset': dataset_meta.to_son()
        }
        return dataset_meta.id

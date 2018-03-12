import base64
import falcon
import uuid
from falcon.media.validators import jsonschema
import metadata
import storage
from ..schema.dataset import DATASET_SCHEMA

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
            dataset_meta = metadata.Dataset.objects.get({'_id': str(id)})
        except metadata.Dataset.DoesNotExist:
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

        resp.media = {'id': dataset_meta.id}

    def dataset_already_uploaded(self, req, resp):
        resp.status = falcon.HTTP_405
        resp.media = {
            'error': 'Dataset already uploaded'
        }

    def upload_dataset(self, req, resp):
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
                'error': 'Dataset metadata does not exist'
            }

    @jsonschema.validate(DATASET_SCHEMA)
    def create_dataset_meta(self, req, resp):
        meta = req.media.copy()
        del meta['is_public']
        document = {
            'is_public': req.media['is_public'],
            'meta': meta
        }
        dataset_meta = metadata.Dataset.from_document(document)
        dataset_meta.id = uuid.uuid4().hex
        dataset_meta.url = dataset_meta.id
        dataset_meta.meta.owner = '0'
        dataset_meta.save()
        resp.status = falcon.HTTP_200
        resp.media = {
            'dataset': dataset_meta.to_son()
        }

import uuid
import falcon
from falcon.media.validators import jsonschema

import metadata
from ..schema.model import MODEL_SCHEMA

__all__ = [
    'ModelResource'
]


class ModelResource:
    def on_get(self, req, resp, id=None):
        if id:
            self.get_model_meta(req, resp, id)
        else:
            self.get_description(req, resp)

    def get_model_meta(self, req, resp, id):
        try:
            model_meta = metadata.Model.objects.get({'_id': str(id)})
        except metadata.Model.DoesNotExist:
            model_meta = None

        if model_meta:
            resp.status = falcon.HTTP_200
            resp.media = {
                'id': model_meta.id,
                'is_public': model_meta.is_public,
                'hash': model_meta.hash,
                'owner': model_meta.meta.owner,
                'size': model_meta.meta.size,
                'date': model_meta.meta.date,
                'title': model_meta.meta.title,
                'description': model_meta.meta.description,
                'category': model_meta.meta.category,
                'labels': model_meta.meta.labels,
                'accuracy': model_meta.meta.accuracy,
                'dataset': model_meta.meta.dataset
            }
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Model metadata does not exist'
            }

    def get_description(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = {
            'description': 'Create model metadata'
        }

    def on_post(self, req, resp, id=None):
        if id:
            self.update_model_meta(req, resp, id)
        else:
            self.create_model_meta(req, resp)

    def update_model_meta(self, req, resp, id):
        try:
            model_meta = metadata.Model.objects.get({'_id': str(id)})
        except metadata.Model.DoesNotExist:
            model_meta = None

        if model_meta:
            resp.status = falcon.HTTP_404
            resp.media = {
                'description': 'Can\'t update model'
            }
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Model metadata does not exist'
            }


    @jsonschema.validate(MODEL_SCHEMA)
    def create_model_meta(self, req, resp):
        # request to document mapping
        meta = req.media.copy()
        del meta['is_public']
        document = {
            'is_public': req.media['is_public'],
            'meta': meta
        }

        # save model metadata to database
        model_meta = metadata.Model.from_document(document)
        model_meta.id = uuid.uuid4().hex
        model_meta.url = model_meta.id
        model_meta.meta.owner = '0'
        model_meta.save()

        resp.status = falcon.HTTP_200
        resp.media = {
            'id': model_meta.id
        }

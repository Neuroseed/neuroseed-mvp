import uuid
import falcon
from falcon.media.validators import jsonschema

import metadata
from .schema import MODEL_SCHEMA

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
            resp.media = {
                'success': True,
                'model': model_meta.to_son()
            }
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                'success': False,
                'error': 'Model metadata does not exist'
            }

    def get_description(self, req, resp):
        resp.media = {
            'success': True,
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
                'success': False,
                'description': 'Can\'t update model'
            }
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                'success': False,
                'error': 'Model metadata does not exist'
            }


    @jsonschema.validate(MODEL_SCHEMA)
    def create_model_meta(self, req, resp):
        model_meta = metadata.Model.from_document(req.media)
        model_meta.id = uuid.uuid4()
        model_meta.url = model_meta.id
        model_meta.save()

        resp.media = {
            'success': True,
            'model': model_meta.to_son()
        }


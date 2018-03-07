import uuid
import falcon
from falcon.media.validators import jsonschema

import metadata
from .schema import ARCHITECTURE_SCHEMA

__all__ = [
    'ArchitectureResource'
]


class ArchitectureResource:
    def on_get(self, req, resp, id=None):
        if id:
            self.get_architecture_meta(req, resp, id)
        else:
            self.get_description(req, resp)

    def get_architecture_meta(self, req, resp, id):
        try:
            architecture = metadata.Architecture.objects.get({'_id': id})
        except metadata.Model.DoesNotExist:
            architecture = None

        if architecture:
            resp.media = {
                'success': True,
                'architecture': architecture.to_son()
            }
        else:
            resp.media = {
                'success': False,
                'error': 'Architecture does not exist'
            }

    def get_description(self, req, resp):
        resp.media = {
            'success': True,
            'description': 'Create architecture'
        }

    def on_post(self, req, resp, id=None):
        if id:
            self.set_architecture(req, resp, id)
        else:
            self.create_architecture(req, resp)

    @jsonschema.validate(ARCHITECTURE_SCHEMA)
    def set_architecture(self, req, resp, id):
        try:
            architecture = metadata.Architecture.objects.get({'id': id})
        except metadata.Model.DoesNotExist:
            architecture = None

        if architecture:
            architecture._set_attributes(req.media)  # TODO: test
            architecture.save()

            resp.media = {
                'success': True
            }
        else:
            resp.media = {
                'success': False,
                'error': 'Architecture does not exist'
            }

    @jsonschema.validate(ARCHITECTURE_SCHEMA)
    def create_architecture(self, req, resp):
        # в функции from_document не происходит маппинг id <-> _id
        req.media['_id'] = req.media['id']  # костыль
        del req.media['id']  # костыль

        architecture = metadata.Architecture.from_document(req.media)
        architecture.id = req.media.get('_id', None) or uuid.uuid4()
        architecture.save()

        resp.media = {
            'success': True,
            'id': architecture.id
        }


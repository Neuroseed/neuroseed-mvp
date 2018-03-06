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
            self.architectutre_meta(req, resp, id)
        else:
            self.description(req, resp)

    def architecture_meta(self, req, resp, id):
        resp.media = {
            'success': True,
            'id': id
        }

    def description(self, req, resp):
        resp.media = {
            'success': True,
            'description': 'text'
        }

    def on_post(self, req, resp, id=None):
        if id:
            self.set_architecture(req, resp, id)
        else:
            self.create_architecture(req, resp)

    @jsonschema.validate(ARCHITECTURE_SCHEMA)
    def set_architecture(self, req, resp, id):
        architecture = metadata.Architecture.objects.get({'id': id})
        architecture._set_attributes(req.media)
        architecture.save()

        resp.media = {
            'success': True
        }

    @jsonschema.validate(ARCHITECTURE_SCHEMA)
    def create_architecture(self, req, resp):
        req.media['_id'] = req.media['id']  # костыль
        del req.media['id']  # костыль

        architecture = metadata.Architecture.from_document(req.media)
        architecture.id = req.media.get('_id', None) or uuid.uuid4()
        architecture.save()

        resp.media = {
            'success': True,
            'id': architecture.id
        }


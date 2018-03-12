import uuid
import falcon
from falcon.media.validators import jsonschema

import metadata
from ..schema.architecture import ARCHITECTURE_SCHEMA

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
            resp.status = falcon.HTTP_200
            resp.media = {
                'id': architecture.id,
                'is_public': architecture.is_public,
                'owner': architecture.owner,
                'title': architecture.title,
                'description': architecture.description,
                'category': architecture.category,
                'architecture': architecture.architecture
            }
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Architecture does not exist'
            }

    def get_description(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = {
            'description': 'Create/get info about architecture'
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

            resp.status = falcon.HTTP_200
            resp.media = {}
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Architecture does not exist'
            }

    @jsonschema.validate(ARCHITECTURE_SCHEMA)
    def create_architecture(self, req, resp):
        id = req.media.get('id', None) or uuid.uuid4().hex

        # в функции from_document не происходит маппинг id <-> _id
        req.media['_id'] = req.media['id']  # костыль
        del req.media['id']  # костыль

        architecture = metadata.Architecture.from_document(req.media)
        architecture.id = id
        architecture.owner = '0'
        architecture.save()

        resp.status = falcon.HTTP_200
        resp.media = {
            'id': id
        }


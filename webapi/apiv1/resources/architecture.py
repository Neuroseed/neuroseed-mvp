import uuid
import logging

import falcon
from falcon.media.validators import jsonschema

import metadata
from ..schema.architecture import ARCHITECTURE_SCHEMA

__all__ = [
    'ArchitectureResource'
]

logger = logging.getLogger(__name__)


class ArchitectureResource:
    auth = {
        'optional_methods': ['GET']
    }

    def on_get(self, req, resp, id=None):
        if id:
            self.get_architecture_meta(req, resp, id)
        else:
            self.get_description(req, resp)

    def get_architecture_meta(self, req, resp, id):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            if user_id:
                kwargs = {'id': id, 'base__owner': user_id}
            else:
                kwargs = {'id': id, 'is_public': True}

            architecture = metadata.ArchitectureMetadata.from_id(**kwargs)
        except metadata.DoesNotExist:
            logger.debug('Architecture {id} does not exist'.format(id=id))

            resp.status = falcon.HTTP_404
            resp.media = {
                'error': 'Architecture does not exist'
            }
            return

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

    def get_description(self, req, resp):
        resp.status = falcon.HTTP_404
        resp.media = {
            'error': 'Architecture does not exist'
        }

    def on_post(self, req, resp, id=None):
        if id:
            self.set_architecture(req, resp, id)
        else:
            self.create_architecture(req, resp)

    @jsonschema.validate(ARCHITECTURE_SCHEMA)
    def set_architecture(self, req, resp, id):
        try:
            architecture = metadata.ArchitectureMetadata.objects(id=id)
        except metadata.DoesNotExist:
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
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        id = req.media.get('id', None) or str(uuid.uuid4())

        architecture = metadata.ArchitectureMetadata(**req.media)
        architecture.id = id
        architecture.owner = user_id
        architecture.save()

        logger.debug('User {uid} create architecture {did}'.format(uid=user_id, did=id))

        resp.status = falcon.HTTP_200
        resp.media = {
            'id': id
        }


import uuid
import logging

import falcon
from falcon.media.validators import jsonschema

import metadata
import manager
from ..schema.architecture import ARCHITECTURE_SCHEMA, CREATE_ARCHITECTURE_SCHEMA

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
            context = {'user_id': user_id}
            architecture = metadata.get_architecture(id, context)
        except metadata.DoesNotExist:
            logger.debug('Architecture {id} does not exist'.format(id=id))

            raise falcon.HTTPNotFound(
                title="Architecture not found",
                description="Architecture metadata does not exist"
            )

        resp.status = falcon.HTTP_200
        architecture_dict = architecture.to_dict()
        result_keys = ['id', 'is_public', 'owner', 'title', 'description', 'category', 'architecture']
        resp.media = {key: architecture_dict[key] for key in result_keys if key in architecture_dict}

    def get_description(self, req, resp):
        raise falcon.HTTPNotFound(
            title="Architecture not found",
            description="Architecture metadata does not exist"
        )

    def on_post(self, req, resp, id=None):
        if id:
            self.set_architecture(req, resp, id)
        else:
            self.create_architecture(req, resp)

    @jsonschema.validate(ARCHITECTURE_SCHEMA)
    def set_architecture(self, req, resp, id):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            architecture = metadata.ArchitectureMetadata.from_id(id=id, owner=user_id)
        except metadata.DoesNotExist:
            architecture = None

        if architecture:
            for key in req.media:
                setattr(architecture, key, req.media[key])
            architecture.save()

            resp.status = falcon.HTTP_200
            resp.media = {}
        else:
            raise falcon.HTTPNotFound(
                title="Architecture not found",
                description="Architecture metadata does not exist"
            )

    @jsonschema.validate(CREATE_ARCHITECTURE_SCHEMA)
    def create_architecture(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        id = req.media.get('id', None) or str(uuid.uuid4())

        with metadata.ArchitectureMetadata().save_context() as architecture:
            architecture.from_dict(req.media)
            architecture.id = id
            architecture.owner = user_id

        logger.debug('User {uid} create architecture {did}'.format(uid=user_id, did=id))

        resp.status = falcon.HTTP_200
        resp.media = {
            'id': id
        }

    @jsonschema.validate(ARCHITECTURE_SCHEMA)
    def on_patch(self, req, resp, id):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            context = {'user_id': user_id}
            manager.update_architecture(id, data=req.media, context=context)
        except metadata.DoesNotExist:
            logger.debug('Architecture {id} does not exist'.format(id=id))

            raise falcon.HTTPNotFound(
                title="Architecture not found",
                description="Architecture metadata does not exist"
            )

        resp.status = falcon.HTTP_204

    def on_delete(self, req, resp, id):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            context = {'user_id': user_id}
            manager.delete_architecture(id, context)
        except metadata.DoesNotExist:
            logger.debug('Architecture {id} does not exist'.format(id=id))

            raise falcon.HTTPNotFound(
                title="Architecture not found",
                description="Architecture metadata does not exist"
            )
        except metadata.errors.ResourcePublishedException:
            raise falcon.HTTPConflict(
                title='Architecture already published',
                description='Can not delete architecture. Architecture already published on blockchain'
            )

        resp.status = falcon.HTTP_200

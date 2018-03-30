import logging

from mongoengine.queryset.visitor import Q
import falcon
import metadata

__all__ = [
    'ArchitecturesResource',
    'ArchitecturesFullResource',
    'ArchitecturesNumberResource'
]

logger = logging.getLogger(__name__)


class ArchitecturesResource:
    def on_get(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        architectures = metadata.ArchitectureMetadata.objects(is_public=True)
        ids = [meta.id for meta in architectures]

        if user_id:
            architectures = metadata.ArchitectureMetadata.objects(is_public=False, owner=user_id)
            ids = [meta.id for meta in architectures] + ids

        resp.status = falcon.HTTP_200
        resp.media = {
            'ids': ids  # response schema v0.2.1
        }


class ArchitecturesFullResource:
    def on_get(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        from_ = int(req.params.get('from', 0))

        if from_ < 0:
            raise falcon.HTTPBadRequest(
                title="Bad Request",
                description="From must be greater than 0"
            )

        number = int(req.params.get('number', 99999))

        if number < 0:
            raise falcon.HTTPBadRequest(
                title="Bad Request",
                description="Number must be greater than 0"
            )

        query = Q(is_public=True)

        if user_id:
            query = query | (Q(is_public=False) & Q(owner=user_id))

        architectures = metadata.ArchitectureMetadata.objects(query).skip(from_).limit(number)
        architectures_meta = self.get_architecture_meta(architectures)

        resp.status = falcon.HTTP_200
        resp.media = {
            'architectures': architectures_meta  # response schema v0.2.2
        }

    @staticmethod
    def get_architecture_meta(architectures):
        architectures_meta = []

        for architecture in architectures:
            architecture_meta = {
                'id': architecture.id,
                'is_public': architecture.is_public,
                'owner': architecture.owner,
                'title': architecture.title,
                'description': architecture.description,
                'category': architecture.category,
                'architecture': architecture.architecture
            }
            architectures_meta.append(architecture_meta)

        return architectures_meta


class ArchitecturesNumberResource:
    def on_get(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        number = metadata.ArchitectureMetadata.objects(is_public=True).count()

        if user_id:
            number += metadata.ArchitectureMetadata.objects(is_public=False, owner=user_id).count()

        resp.status = falcon.HTTP_200
        resp.media = number

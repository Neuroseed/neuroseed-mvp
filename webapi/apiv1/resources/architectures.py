import logging

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

        architectures = metadata.ArchitectureMetadata.objects(is_public=True)
        architectures_meta = self.get_datasets_meta(architectures)

        if user_id:
            architectures = metadata.ArchitectureMetadata.objects(is_public=False, owner=user_id)
            architectures_meta = self.get_datasets_meta(architectures) + architectures_meta

        from_ = int(req.params.get('from', 0))

        if from_ < 0:
            resp.status = falcon.HTTP_400
            resp.media = {'error': 'from must be greater than 0'}
            return

        number = int(req.params.get('number', 99999))

        if number < 0:
            resp.status = falcon.HTTP_400
            resp.media = {'error': 'number must be greater than 0'}
            return

        architectures_meta = architectures_meta[from_: from_ + number]

        resp.status = falcon.HTTP_200
        resp.media = {
            'architectures': architectures_meta  # response schema v0.2.2
        }

    @staticmethod
    def get_datasets_meta(architectures):
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

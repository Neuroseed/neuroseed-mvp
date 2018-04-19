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

        context = {'user_id': user_id}
        architectures = metadata.get_architectures(context)
        ids = [meta.id for meta in architectures]

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

        context = {'user_id': user_id}
        filter = {'from': from_, 'number': number}
        architectures = metadata.get_architectures(context, filter)
        architectures_meta = self.get_architecture_meta(architectures)

        resp.status = falcon.HTTP_200
        resp.media = {
            'architectures': architectures_meta  # response schema v0.2.2
        }

    @staticmethod
    def get_architecture_meta(architectures):
        architectures_meta = []

        for architecture in architectures:
            architecture_dict = architecture.to_dict()
            result_keys = ['id', 'is_public', 'owner', 'title', 'description', 'category', 'architecture']
            architecture_meta = {key: architecture_dict[key] for key in result_keys if key in architecture_dict}
            architectures_meta.append(architecture_meta)

        return architectures_meta


class ArchitecturesNumberResource:
    def on_get(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        context = {'user_id': user_id}
        number = metadata.get_architectures(context).count()

        resp.status = falcon.HTTP_200
        resp.media = number

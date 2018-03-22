import logging

import falcon
import metadata

__all__ = [
    'ModelsResource'
]

logger = logging.getLogger(__name__)


class ModelsResource:
    def on_get(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        models = metadata.ModelMetadata.objects(is_public=True)
        ids = [meta.id for meta in models]

        if user_id:
            models = metadata.ModelMetadata.objects(is_public=False, owner=user_id)
            ids = [meta.id for meta in models] + ids

        resp.status = falcon.HTTP_200
        resp.media = {
            'ids': ids  # response schema v0.2.1
        }

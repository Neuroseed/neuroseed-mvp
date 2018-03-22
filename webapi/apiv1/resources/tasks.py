import logging

import falcon
import metadata

__all__ = [
    'TasksResource'
]

logger = logging.getLogger(__name__)


class TasksResource:
    def on_get(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        tasks = metadata.TaskMetadata.objects(owner=user_id)

        ids = [task.id for task in tasks]

        resp.status = falcon.HTTP_200
        resp.media = {
            'ids': ids  # response schema v0.2.1
        }


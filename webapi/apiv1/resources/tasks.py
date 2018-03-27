import logging

import falcon
import metadata

__all__ = [
    'TasksResource',
    'TasksFullResource',
    'TasksNumberResource'
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


class TasksFullResource:
    def on_get(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        tasks = metadata.TaskMetadata.objects(owner=user_id)
        tasks_meta = self.get_tasks_meta(tasks)

        from_ = int(req.params.get('from', 0))

        if from_ < 0:
            resp.status = falcon.HTTP_400
            resp.media = {'error': 'from must be greater than 0'}

        number = int(req.params.get('number', 99999))

        if number < 0:
            resp.status = falcon.HTTP_400
            resp.media = {'error': 'number must be greater than 0'}

        tasks_meta = tasks_meta[from_: from_ + number]

        resp.status = falcon.HTTP_200
        resp.media = {
            'tasks': tasks_meta  # response schema v0.2.2
        }

    @staticmethod
    def get_tasks_meta(tasks):
        tasks_meta = []

        for task in tasks:
            task_meta = {
                'id': task.id,
                'status': task.status,
                'command': task.command,
                'date': task.date,
                'config': task.config
            }
            tasks_meta.append(task_meta)

        return tasks_meta


class TasksNumberResource:
    def on_get(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        number = metadata.TaskMetadata.objects(owner=user_id).count()

        resp.status = falcon.HTTP_200
        resp.media = number

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

        context = {'user_id': user_id}
        tasks = metadata.get_tasks(context)

        ids = [task.id for task in tasks]

        resp.status = falcon.HTTP_200
        resp.media = {
            'ids': ids  # response schema v0.2.1
        }


class TasksFullResource:
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
        tasks = metadata.get_tasks(context, filter)
        tasks_meta = self.get_tasks_meta(tasks)

        resp.status = falcon.HTTP_200
        resp.media = {
            'tasks': tasks_meta  # response schema v0.2.2
        }

    @staticmethod
    def get_tasks_meta(tasks):
        tasks_meta = []

        for task in tasks:
            task_dict = task.to_dict()
            result_keys = ['id', 'status', 'command', 'date', 'config']
            task_meta = {key: task_dict[key] for key in result_keys if key in task_dict}
            tasks_meta.append(task_meta)

        return tasks_meta


class TasksNumberResource:
    def on_get(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        context = {'user_id': user_id}
        number = metadata.get_tasks(context).count()

        resp.status = falcon.HTTP_200
        resp.media = number

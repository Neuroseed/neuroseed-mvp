import falcon
import metadata

__all__ = [
    'TasksResource'
]


class TasksResource:
    def on_get(self, req, resp):
        tasks = metadata.Task.objects.all()

        tasks_ids = [task.id for task in tasks]

        resp.status = falcon.HTTP_200
        resp.media = {
            'success': True,
            'models': tasks_ids
        }


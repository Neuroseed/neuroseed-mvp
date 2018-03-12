import falcon
import metadata

__all__ = [
    'TasksResource'
]


class TasksResource:
    def on_get(self, req, resp):
        tasks = metadata.TaskMetadata.objects.all()

        tasks_ids = [task.id for task in tasks]

        resp.status = falcon.HTTP_200
        resp.media = {
            'tasks': tasks_ids
        }


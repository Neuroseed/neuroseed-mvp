import falcon
import metadata

__all__ = [
    'TasksResource'
]


class TasksResource:
    def on_get(self, req, resp):
        tasks = metadata.TaskMetadata.objects.all()

        ids = [task.id for task in tasks]

        resp.status = falcon.HTTP_200
        resp.media = {
            'ids': ids  # response schema v0.2.1
        }


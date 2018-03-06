import falcon
import metadata

__all__ = [
    'ModelsResource'
]


class ModelsResource:
    def on_get(self, req, resp):
        models_meta = metadata.Model.objects.all()

        models_ids = [meta.id for meta in models_meta]

        resp.status = falcon.HTTP_200
        resp.media = {
            'success': True,
            'models': models_ids
        }


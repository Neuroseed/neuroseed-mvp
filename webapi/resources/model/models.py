import falcon
import metadata

__all__ = [
    'ModelsResource'
]


class ModelsResource:
    def on_get(self, req, resp):
        models_meta = metadata.ModelMetadata.objects.all()

        ids = [meta.id for meta in models_meta]

        resp.status = falcon.HTTP_200
        resp.media = {
            'ids': ids  # response schema v0.2.1
        }


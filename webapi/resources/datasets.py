import falcon
import metadata

__all__ = [
    'DatasetsResource'
]


class DatasetsResource:
    def on_get(self, req, resp):
        datasets = metadata.DatasetMetadata.objects.all()
        ids = [meta.id for meta in datasets]

        resp.status = falcon.HTTP_200
        resp.media = {
            'ids': ids  # response schema v0.2.1
        }

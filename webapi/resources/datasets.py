import falcon
import metadata

__all__ = [
    'DatasetsResource'
]


class DatasetsResource:
    def on_get(self, req, resp):
        datasets = metadata.DatasetMetadata.objects.all()
        datasets_ids = [meta.id for meta in datasets]

        resp.status = falcon.HTTP_200
        resp.media = {
            'datasets': datasets_ids
        }

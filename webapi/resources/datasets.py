
__all__ = [
    'DatasetsResource'
]


class DatasetsResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = {
            'success': True,
            'datasets': []
        }


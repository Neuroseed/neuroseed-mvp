import falcon

__all__ = [
    'ModelsResource'
]


class ModelsResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = {
            'success': True,
            'models': []
        }


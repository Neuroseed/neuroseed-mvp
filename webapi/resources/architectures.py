import falcon

__all__ = [
    'ArchitecturesResource'
]


class ArchitecturesResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.media = {
            'success': True,
            'datasets': []
        }


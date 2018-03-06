import falcon

__all__ = [
    'ArchitectureResource'
]


class ArchitectureResource:
    def on_get(self, req, resp, id=None):
        if id:
            self.architectutre_meta(req, resp, id)
        else:
            self.description(req, resp)

    def architecture_meta(self, req, resp, id):
        resp.media = {
            'success': True,
            'id': id
        }

    def description(self, req, resp):
        resp.media = {
            'success': True,
            'description': 'text'
        }

    def on_post(self, req, resp, id=None):
        if id:
            self.create_architecture(req, resp, id)
        else:
            self.init_architecture(req, resp)

    def create_architecture(self, req, resp, id):
        pass

    def init_architecture(self, req, resp):
        pass


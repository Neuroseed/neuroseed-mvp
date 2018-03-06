import falcon
__all__ = [
    'ModelResource'
]


class ModelResource:
    def on_get(self, req, resp, id=None):
        if id:
            self.get_model_meta(req, resp, id)
        else:
            self.get_description(req, resp)

    def get_model_meta(self, req, resp, id):
        resp.media = {
            'success': True,
            'id': id
        }

    def get_description(self, req, resp):
        resp.media = {
            'success': True,
            'description': 'text'
        }

    def on_post(self, req, resp, id=None):
        if id:
            self.train_model(req, resp, id)
        elif id:
            self.test_model(req, resp, id)
        elif id:
            self.predict_model(req, resp, id)
        else:
            self.create_model(req, resp)

    def train_model(self, req, resp, id):
        resp.media = {
            'success': True,
            'description': 'text'
}

    def test_model(self, req, resp, id):
        resp.media = {
            'success': True,
            'description': 'text'
}

    def predict_model(self, req, resp, id):
        resp.media = {
            'success': True,
            'description': 'text'
}

    def create_model(self, req, resp):
        resp.media = {
            'success': True,
            'description': 'text'
}


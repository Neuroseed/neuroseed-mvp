
__all__ = [
    'DatasetResource'
]


class DatasetResource:
    def on_get(self, req, resp, id=None):
        if id:
            self.get_dataset_meta(req, resp, id)
        else:
            self.get_description(req, resp)

    def get_dataset_meta(self, req, resp, id):
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
            self.upload_dataset(req, resp, id)
        else:
            self.init_dataset(req, resp)

    def upload_dataset(self, req, resp, id):
        pass

    def init_dataset(self, req, resp):
        pass


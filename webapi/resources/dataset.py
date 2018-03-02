
__all__ = [
    'DatasetResource'
]


class DatasetResource:
    def on_get(self, req, resp, id=None):
        if id:
            self.on_get_dataset_meta(req, resp, id)
        else:
            self.on_description(req, resp)

    def on_get_dataset_meta(self, req, resp, id):
        resp.media = {
            'success': True,
            'id': id
        }

    def on_description(self, req, resp):
        resp.media = {
            'success': True,
            'description': 'text'
        }

    def on_post(self, req, resp, id=None):
        if id:
            self.on_upload_dataset(req, resp, id)
        else:
            self.on_init_dataset(req, resp)

    def on_upload_dataset(self, req, resp, id):
        pass

    def on_init_dataset(self, req, resp):
        pass


import base64
import metadata
import storage
import falcon

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
        try:
            dataset = metadata.Dataset.objects.get({'_id': str(id)})
        except metadata.Dataset.DoesNotExist:
            dataset = None

        if dataset:
            url = dataset.url
            file_path = storage.get_dataset_path(url)
            with open(file_path, 'wb') as f:
                data = base64.b64decode(req.media)
                f.write(data)

            resp.media = {'success': True}
        else:
            resp.status = falcon.HTTP_404
            resp.media = {
                'success': False,
                'error': 'Dataset metadata does not exist'
            }

    def init_dataset(self, req, resp):
        pass


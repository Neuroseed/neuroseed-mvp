import falcon
from falcon import media
from .resources import *


class TextPlainHandler(media.BaseHandler):
    """
    Обработчик текстовых данных типа
    MIME text/plain
    """

    def serialize(self, obj):
        return obj

    def deserialize(self, raw):
        return raw


def configure_api_v1(api):
    BASE = '/api/v1/'

    datasets_resource = DatasetsResource()
    api.add_route(BASE + 'datasets', datasets_resource)

    dataset_resource = DatasetResource()
    api.add_route(BASE + 'dataset', dataset_resource)
    api.add_route(BASE + 'dataset/{id}', dataset_resource)


def main():
    api = falcon.API()
    extra_handlers = {
        'text/plain': TextPlainHandler()
    }
    api.req_options.media_handlers.update(extra_handlers)

    configure_api_v1(api)

    return api


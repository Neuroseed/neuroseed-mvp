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

    # dataset operations
    dataset_resource = DatasetResource()
    api.add_route(BASE + 'dataset', dataset_resource)
    api.add_route(BASE + 'dataset/{id}', dataset_resource)

    # list of datasets
    datasets_resource = DatasetsResource()
    api.add_route(BASE + 'datasets', datasets_resource)

    # architecture operations
    architecture_resource = ArchitectureResource()
    api.add_route(BASE + 'architecture', architecture_resource)
    api.add_route(BASE + 'architecture/{id}', architecture_resource)

    # list of architectures
    architectures_resource = ArchitecturesResource()
    api.add_route(BASE + 'architectures', architectures_resource)
 
    # model operation
    model_resource = ModelResource()
    api.add_route(BASE + 'model', model_resource)
    api.add_route(BASE + 'model/{id}', model_resource)

    # list of models
    models_resource = ModelsResource()
    api.add_route(BASE + 'models', models_resource)

    # task operation
    task_resource = TaskResource()
    api.add_route(BASE + 'task/{id}', task_resource)
    api.add_route(BASE + 'task', task_resource)

    # tasks list
    tasks_resource = TasksResource()
    api.add_route(BASE + 'tasks', tasks_resource)


def main():
    api = falcon.API()
    extra_handlers = {
        'text/plain': TextPlainHandler()
    }
    api.req_options.media_handlers.update(extra_handlers)

    configure_api_v1(api)

    return api


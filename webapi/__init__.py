import falcon
from .resources import *

BASE = '/api/v1/'


def configure_api_v1(api):

#list of datasets
    datasets_resource = DatasetsResource()
    api.add_route(BASE + 'datasets', datasets_resource)

#dataset operations
    dataset_resource = DatasetResource()
    api.add_route(BASE + 'dataset', dataset_resource)
    api.add_route(BASE + 'dataset/{id}', dataset_resource)
    api.add_route(BASE + 'dataset/create_dataset_meta/{id}', dataset_resource)

#architecture operations
    architecture_resource = ArchitectureResource()
    api.add_route(BASE + 'architecture', architecture_resource)
    api.add_route(BASE + 'architecture/{id}', architecture_resource)

#list of architectures
    architectures_resource = ArchitecturesResource()
    api.add_route(BASE + 'architectures', architectures_resource)

#list of models
    models_resource = ModelsResource
    api.add_route(BASE + 'models', models_resource)
    
#model operation
    model_resource = ModelResource()
    api.add_route(BASE + 'model', model_resource)
    api.add_route(BASE + 'model/train_model/{id}', model_resource)
    api.add_route(BASE + 'model/test_model/{id}', model_resource)
    api.add_route(BASE + 'model/predict_model/{id}', model_resource)
    api.add_route(BASE + 'model/create_model', model_resource)


def main():
    api = falcon.API()

    configure_api_v1(api)

    return api


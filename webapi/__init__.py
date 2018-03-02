import falcon
from .resources import *

BASE = '/api/v1/'


def configure_api_v1(api):
    datasets_resource = DatasetsResource()
    api.add_route(BASE + 'datasets', datasets_resource)

    dataset_resource = DatasetResource()
    api.add_route(BASE + 'dataset', dataset_resource)
    api.add_route(BASE + 'dataset/{id}', dataset_resource)


def main():
    api = falcon.API()

    configure_api_v1(api)

    return api


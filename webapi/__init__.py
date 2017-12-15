import json
from pyramid.config import Configurator
import worker


def configure_api_v1(config):
    api_v = '/api/v1'
    config.add_route('api_v1', api_v)

    config.add_route('api_v1_user', api_v + '/user')
    config.add_route('api_v1_login', api_v + '/login')
    config.add_route('api_v1_token_refresh', api_v + '/token/refresh')
    
    config.add_route('api_v1_datasets', api_v + '/datasets')
    config.add_route('api_v1_dataset_empty', api_v + '/dataset')
    config.add_route('api_v1_dataset', api_v + '/dataset/{id}')

    config.add_route('api_v1_architectures', api_v + '/architectures')
    config.add_route('api_v1_architecture_empty', api_v + '/architecture')
    config.add_route('api_v1_architecture', api_v + '/architecture/{id}')

    config.add_route('api_v1_models', api_v + '/models')
    config.add_route('api_v1_model_empty', api_v + '/model')
    config.add_route('api_v1_model', api_v + '/model/{id}')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    configure_api_v1(config)

    with open('celery_config.json') as f:
        celery_config = json.load(f)
        print(celery_config)
        worker.app.config_from_object(celery_config)

    config.registry.tasker = worker

    config.scan()
    return config.make_wsgi_app()


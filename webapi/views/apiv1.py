import jwt
from pyramid.view import view_config

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'


@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'webapi'}


@view_config(route_name='api_v1', renderer='json')
def api_v1(request):
    return {'status': True}


@view_config(route_name='api_v1_user', renderer='json')
def user(request):
    authorization = request.headers['Authorization']
    data = jwt.decode(authorization, JWT_SECRET, algorithm=JWT_ALGORITHM)
    print(data)
    return {}


@view_config(route_name='api_v1_login', renderer='json')
def login(request):
    import random
    user_id = random.randint(0, 1024)

    data = {'role': 'user', 'user_id': user_id}
    key = 'secret'
    token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
    token = token.decode('utf-8')

    data = {'role': 'user', 'refresh': True, 'user_id': user_id}
    key = 'secret'
    refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
    refresh_token = refresh_token.decode('utf-8')

    data = {
        'token': token,
        'refresh': refresh_token
    }
    return data


@view_config(route_name='api_v1_token_refresh', renderer='json')
def token_refresh(request):
    if 'refresh' in request.GET:
        raw_refresh = request.GET['refresh']
        data = jwt.decode(raw_refresh, JWT_SECRET, algorithm=JWT_ALGORITHM)
        if 'refresh' in data:
            print(data)
            return {
                'error': False,
                'token': '',
                'refresh': ''
            }

    return {
        'error': True,
        'message': 'Endpoin /api/v1/token/refresh need refresh token'
    }


@view_config(route_name='api_v1_datasets', renderer='json')
def datasets(request):
    # print(request.headers)
    # print(request.params)  # get + post
    # print(request.GET)  # query
    # print(request.POST)  # body args

    # tasker = request.registry.tasker
    # task = tasker.get_datasets.delay()
    # data = task.get(timeout=5)

    metadata = request.registry.metadata
    data = metadata.get_datasets()

    return data


@view_config(route_name='api_v1_dataset_empty', renderer='json')
def dataset_empty(request):
    data = {
        'error': True,
        'message': 'Endpoint /api/v1/dataset/{id} need id parameter!'
    }
    return data


@view_config(route_name='api_v1_dataset', renderer='json')
def dataset(request):
    return {}


@view_config(route_name='api_v1_architectures', renderer='json')
def architectures(request):
    return {'architectures': []}


@view_config(route_name='api_v1_architecture_empty', renderer='json')
def architecture_empty(request):
    data = {
        'error': True,
        'message': 'Endpoint /api/v1/architecture/{id} need id parameter!'
    }
    return data


@view_config(route_name='api_v1_architecture', renderer='json')
def architecture(request):
    print(request.matchdict['id'])
    return {}


@view_config(route_name='api_v1_models', renderer='json')
def models(request):
    metadata = request.registry.metadata
    data = metadata.get_models()

    return data


@view_config(route_name='api_v1_model_empty', renderer='json')
def model_empty(request):
    data = {
        'error': True,
        'message': 'Endpoint /api/v1/model/{id} need id parameter!'
    }
    return data


@view_config(route_name='api_v1_model', renderer='json')
def model(request):
    print(request.matchdict['id'])
    return {}


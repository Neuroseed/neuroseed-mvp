from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'webapi'}


@view_config(route_name='api_v1', renderer='json')
def api_v1(request):
    return {'status': True}


@view_config(route_name='api_v1_getdatasets', renderer='json')
def api_v1_getdatasets(request):
    return {'datasets': []}


@view_config(route_name='api_v1_getmodels', renderer='json')
def api_v1_getmodels(request):
    return {'models': []}


@view_config(route_name='api_v1_getarchs', renderer='json')
def api_v1_getarchs(request):
    return {'archs': []}


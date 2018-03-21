import falcon
from falcon_auth import FalconAuthMiddleware


class NeuroseedAuthMiddleware(FalconAuthMiddleware):
    """
    Resource auth schema:
    auth = {
        inherit FalconAuthMiddleware auth schema,
        'optional_routes': []
        'optional_methods': []
    }
    """

    def __init__(self, backend, exempt_routes=None, exempt_methods=None
, optional_routes=None, optional_methods=None):
        super().__init__(backend, exempt_routes, exempt_methods)

        self.optional_routes = list(optional_routes or [])
        self.optional_methods = list(optional_methods or [])

    def process_resource(self, req, resp, resource, *args, **kwargs):
        auth_setting = self._get_auth_settings(req, resource)
        try:
            super().process_resource(req, resp, resource, *args, **kwargs)
        except falcon.HTTPUnauthorized:
            optional_routes = tuple(self.optional_routes) + tuple(auth_setting.get('optional_routes', ()))
            optional_methods = tuple(self.optional_methods) + tuple(auth_setting.get('optional_methods', ()))

            if req.path in optional_routes or \
               req.method in optional_methods:
                req.context['user'] = None
            else:
                raise

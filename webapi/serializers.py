import json

import falcon


def falcon_error_serializer(_: falcon.Request, resp: falcon.Response, exc: falcon.HTTPError) -> None:
    """ Serializer for native falcon HTTPError exceptions.

    Serializes HTTPError classes as proper json:api error
        see: http://jsonapi.org/format/#errors
    """
    error = {
        'title': exc.title,
        'error': exc.description,
        'status': int(exc.status[0:3]),
    }

    if hasattr(exc, "link") and exc.link is not None:
        error['links'] = {'about': exc.link['href']}

    resp.body = json.dumps(error)

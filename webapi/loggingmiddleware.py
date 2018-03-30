import json


class LoggingMidleware:
    def __init__(self, logger):
        self.logger = logger

    def process_request(self, req, resp):
        content_type = req.content_type
        content_length = req.content_length
        relative_uri = req.relative_uri
        method = req.method
        scheme = req.scheme
        headers = req.headers
        headers_json = json.dumps(headers, indent=2)
        params = req.params

        self.logger.info('Request {scheme} {method} {relative_uri}\n'
                    'Content Type: {content_type}\n'
                    'Content Length: {content_length}\n'
                    'Params: {params}\n'
                    'Headers: {headers}'.format(
            scheme=scheme,
            method=method,
            relative_uri=relative_uri,
            content_type=content_type,
            content_length=content_length,
            params=params,
            headers=headers_json))

    def process_response(self, req, resp, resource, req_succeeded):
        content_type = resp.content_type
        status = resp.status

        self.logger.info('Response\n'
                    'Content Type: {content_type}\n'
                    'Status: {status}'.format(
            content_type=content_type,
            status=status))

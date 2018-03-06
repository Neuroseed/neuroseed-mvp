import json
import webapi
import metadata
import storage

api = webapi.main()


def serve_forever():
    with open('config/falcon_config.json') as f:
        config = json.load(f)

    host = config['host']
    port = config['port']

    httpd = simple_server.make_server(host, port, api)
    print('Start server on {}:{}'.format(host, port))
    httpd.serve_forever()


if __name__ == '__main__':
    from wsgiref import simple_server

    metadata.from_config('config/metadata_config.json')
    storage.from_config('config/storage_config.json')

    serve_forever()


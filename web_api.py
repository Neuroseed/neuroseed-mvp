import json
import webapi

api = webapi.main()


if __name__ == '__main__':
    from wsgiref import simple_server

    with open('falcon_config.json') as f:
        config = json.load(f)

    host = config['host']
    port = config['port']

    httpd = simple_server.make_server(host, port, api)
    print('Start server on {}:{}'.format(host, port))
    httpd.serve_forever()


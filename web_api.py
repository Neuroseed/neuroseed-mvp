from gevent import monkey
monkey.patch_all()

import webapi

webapi.init_logging()
config = webapi.from_config('config/web_api_config.json')
api = webapi.main(config)

if __name__ == '__main__':
    webapi.serve_forever(api, config)

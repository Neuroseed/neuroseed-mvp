import worker


worker.from_config('config/worker_config.json')
worker.main()

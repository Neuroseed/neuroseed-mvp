import worker
from worker import app  # don't delete: used in celery cli


worker.from_config('config/worker_config.json')

if __name__ == '__main__':
    worker.main()

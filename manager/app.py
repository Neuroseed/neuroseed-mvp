import json
import celery

app = celery.Celery('tasks')


def configure(filepath):
    with open('config/celery_config.json') as f:
        celery_config = json.load(f)
        app.config_from_object(celery_config)

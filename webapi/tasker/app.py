import celery

app = celery.Celery('tasks')

'''
config = {
    'broker_url': 'pyamqp://guest@192.168.0.108//',
    'result_backend': 'rpc://',
    'result_expires': 3600,
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json'],
    'timezone': 'Europe/Oslo',
    'enable_utc': True
}

app.conf.update(config)
'''

app.config_from_object('celeryconfig')


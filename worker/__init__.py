import json

from .tasks import *
from .app import app


def from_config(config_file):
    with open(config_file) as f:
        celery_config = json.load(f)
        app.config_from_object(celery_config)

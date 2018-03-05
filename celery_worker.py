import sys
import json
import celery
from webapi.tasker import *

with open('celery_config.json') as f:
        celery_config = json.load(f)
        app.config_from_object(celery_config)

sys.argv.extend(['-l', 'info'])
app.worker_main()


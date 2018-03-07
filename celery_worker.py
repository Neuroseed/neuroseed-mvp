import sys
import json
import celery

import metadata
from worker.app import *

with open('config/celery_config.json') as f:
        celery_config = json.load(f)
        app.config_from_object(celery_config)

metadata.from_config('config/metadata_config.json')

sys.argv.extend(['-l', 'info'])
app.worker_main()


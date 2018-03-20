import sys
import json

import metadata
import storage
import worker
from worker.app import *

metadata.from_config('config/metadata_config.json')
storage.from_config('config/storage_config.json')
worker.from_config('config/celery_config.json')

with open('config/worker_config.json') as f:
        config = json.load(f)

log_level = config['log_level']
sys.argv.extend(['-l', log_level])
sys.argv.append('--autoscale=10,1')
app.worker_main()

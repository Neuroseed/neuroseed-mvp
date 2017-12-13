import sys
import celery
from webapi.tasker import *

sys.argv.extend(['-l', 'info'])
app.worker_main()


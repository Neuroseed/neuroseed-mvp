import sys
import json

from flower.__main__ import main

with open('config/celery_config.json', 'r') as f:
    config = json.load(f)

sys.argv.append('--debug=True')
# sys.argv.append('--broker={broker_url}'.format(broker_url=config['broker_url']))
sys.argv.append('--broker=pyamqp://guest@rabbitmqserver:5672//')

main()

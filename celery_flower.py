import sys
import json

from flower.__main__ import main

with open('config/flower_config.json', 'r') as f:
    config = json.load(f)

auth = ','.join(['%s:%s' % (u, p) for u, p in config['users'].items()])

sys.argv.append('--debug=True')
# sys.argv.append('--broker={broker_url}'.format(broker_url=config['broker_url']))
sys.argv.append('--broker=pyamqp://guest@rabbitmqserver:5672//')
sys.argv.append('--basic_auth=%s' % auth)

main()

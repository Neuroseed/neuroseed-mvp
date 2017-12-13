# Neuroseed Platform Alpha - WEB API

Release Version 0.1.0

## Dependencies

* pyramid==1.9.1
* celry==4.1.0

## Development

Start REST API server:

```bash
pserve development.ini --reload
```

Start celery worker:

```bash
python3 celery_worker.py
```

Celery worker configuration file: repo/celeryconfig.py

Start rabbitmq server (version 3.7.0):

```bash
docker run -d --rm --net=host --name rabbitmq rabbitmq:3.7.0
```

### Tests

Install dependencies:

```bash
pip3 install -e ".[testing]"
```

Run tests:

```bash
pytest -q
```

## Production

```bash
pserve production.ini --reload
```

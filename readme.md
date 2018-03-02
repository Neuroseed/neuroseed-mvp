# Neuroseed MVP

Release Version 0.1.0

## Dependencies

* falcon=1.4.1
* celery==4.1.0
* pymongo==3.6.0
* PyJWT==1.5.3

## Install Dependencies

```bahs
virtualenv venv
. venv/bin/activate
python3 setup.py develop
```

## Development

Start web api server:

```bash
python3 web_api.py
```

Start celery worker:

```bash
python3 celery_worker.py
```

Celery worker configuration file: repo/celery_config.json

Start rabbitmq server (version 3.7.0):

```bash
docker run -d --rm --net=host --name rabbitmq rabbitmq:3.7.0
```

**Start Mongo Database server with Docker:**

Create volume:

```bash
docker volume create mongov
```

Run mongodb container:

```bash
docker run -d --rm --net=host -v mongov:/data/db --name mongo mongo:3.6.0
```

Run mongodb container with authentication:

```bash
docker run -d --rm --net=host -v mongov:/data/db --name mongo mongo:3.6.0 --auth
```


## Production

```bash
gunicorn web_api:api
```

# Neuroseed MVP

Release Version 0.3.2

## Dependencies

* celery==4.1.0
* pymongo==3.6.0
* mongoengine==0.15.0
* falcon==1.4.1
* jsonschema==2.6.0
* PyJWT==1.6.0
* falcon-auth==1.1.0
* falcon-cors==1.1.7
* gevent==1.2.2

## Install Dependencies

### WEB API Dependencies

```bahs
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
```

### Worker Dependencies

```bahs
python3 -m venv venv
. venv/bin/activate
pip3 install -r worker-requirements.txt
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

Celery worker configuration file: *config/celery_config.json*

### Start rabbitmq server (version 3.7.0)

```bash
source docker/start-rabbitmq.sh
```

### Start Mongo Database server with Docker

Create volume:

```bash
docker volume create mongov
```

Run mongodb container:

```bash
source docker/start-mongo.sh
```

## Stop rabbitmq and mongodb

```bash
docker kill rabbitmq
docker kill mongo
```

## Usage examples

Example scripts in *examples* directory.

For example create upload cifar10 dataset:

```bash
python3 examples/upload_cifar10.py
```

For example train neural network on cifar10 dataset:

```bash
python3 examples/train_cnn_cifar10.py
```

## Unit Tests

Install tests dependencies:

```bash
pip3 install -e .[testing]
```

Start unit tests by **bash** commands:

```bash
python3 setup.py test
```


## Production

Replace authentication key: *config/auth.key*

Replace certificates in *config/celery_ssl* and *config/rabbitmq*

Add users for rbbitmq: *config/rabbitmq/rabbitmq.conf*

Edit config files in *config* directory

## Logging

Logs saved in *logs* directory.

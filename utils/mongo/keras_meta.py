"""
Keras datasets:
* mnist     - ok
* cifar10   - ok
* cifar100  - ok
* imdb
* reuters
* fashion_mnist
* boston_housing

Keras models:
* vgg16     - ok
* resnet50
* vgg19
* inception_v3
* xception
* inception_resnet_v2
* mobilenet
"""

import json
import hashlib
import pymongo
from pymongo.errors import InvalidOperation


def get_config():
    with open('metadata_config.json') as f:
        config = json.load(f)

    return config


def get_meta_mnist():
    name = 'mnist'
    hash = hashlib.sha256(name.encode('utf-8')).hexdigest()

    meta = {
        'id': name,
        'uri': 'urn:keras:%s' % name,
        'hash': hash,
        'size': (24, 24),
        'classes': 10,
        'labels': [str(n) for n in range(10)]
    }

    return meta


def get_meta_cifar10():
    name = 'cifar10'
    hash = hashlib.sha256(name.encode('utf-8')).hexdigest()

    meta = {
        'id': name,
        'uri': 'urn:keras:%s' % name,
        'hash': hash,
        'size': (32, 32, 3),
        'classes': 10,
        'labels': [
            'airplane',
            'automobile',
            'bird',
            'cat',
            'deer',
            'dog',
            'frog',
            'horse',
            'ship',
            'truck'
        ]
    }

    return meta


def get_meta_cifar100():
    name = 'cifar100'
    hash = hashlib.sha256(name.encode('utf-8')).hexdigest()

    meta = {
        'id': name,
        'uri': 'urn:keras:%s' % name,
        'hash': hash,
        'size': (32, 32, 3),
        'classes': 100,
        'labels': [str(n) for n in range(100)]
    }

    return meta


def get_meta_vgg16():
    name = 'vgg16'
    hash = hashlib.sha256(name.encode('utf-8')).hexdigest()

    meta = {
        'id': name,
        'uri': 'urn:keras:%s' % name,
        'hash': hash,
        'input_size': (224, 224, 3),
        'classes': 10,
        'labels': [str(n) for n in range(100)]
    }

    return meta


def get_datasets_meta():
    datasets_id = [
        'mnist',
        'cifar10',
        'cifar100',
    ]

    datasets_meta = []

    for name in datasets_id:
        g = globals()
        meta = g['get_meta_%s' % name]()
        datasets_meta.append(meta)

    return datasets_meta


def get_models_meta():
    models_id = [
        'vgg16',
    ]

    models_meta = []

    for name in models_id:
        g = globals()
        meta = g['get_meta_%s' % name]()
        models_meta.append(meta)

    return models_meta


def init_mongo_meta(local=False):
    if local:
        url = 'mongodb://localhost'
    else:
        config = get_config()
        url = config['mongo_url']

    # metadata
    datasets_meta = get_datasets_meta()
    print(datasets_meta)

    models_meta = get_models_meta()
    print(models_meta)

    # mongo
    client = pymongo.MongoClient(url)

    metadata = client.metadata

    # save datasets metadata
    metadata.drop_collection('datasets')
    datasets = metadata.datasets
    print('Save datasets metadata...')
    try:
        datasets.insert(datasets_meta)
        print('Datasets metadata saved.')
        print('Datasets metadata count:', datasets.count())
    except InvalidOperation:
        print('Datasets metadata don\'t saved')
        raise

    # save models metadata
    metadata.drop_collection('models')
    models = metadata.models
    print('Save models metadata...')
    try:
        models.insert(models_meta)
        print('Models metadata saved.')
        print('Models metadata count:', models.count())
    except InvalidOperation:
        print('Models metadata don\'t saved')
        raise


if __name__ == '__main__':
    init_mongo_meta(True)

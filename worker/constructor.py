from keras import models
from keras import layers
from keras import optimizers


def create_model(architecture, shape):
    if not type(architecture) is dict:
        raise TypeError('type of architecture must be dict')

    if not type(shape) in (tuple, list):
        raise TypeError('shape must be iterable')

    shape = tuple(shape)

    if len(shape) == 0:
        raise ValueError('len of shape must be greater than zero')

    input = output = layers.Input(shape=shape)

    for layer in architecture['layers']:
        name = layer['name']
        config = layer.get('config', {})
        output = getattr(layers, name)(**config)(output)

    return models.Model(inputs=input, outputs=output)


def compile_model(model, config):
    # compile
    loss = config['loss']
    optimizer_name = config['optimizer']['name']
    optimizer_config = config['optimizer'].get('config', {})
    optimizer = getattr(optimizers, optimizer_name)(**optimizer_config)
    metrics = config.get('metrics', [])
    metrics.append('accuracy')

    # compile keras model
    model.compile(
        loss=loss,
        optimizer=optimizer,
        metrics=metrics)

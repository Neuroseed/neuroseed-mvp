from keras import models
from keras import layers
from keras import optimizers


def create_model(architecture, shape):
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
    optimizer_config = config['optimizer']['config']
    optimizer = getattr(optimizers, optimizer_name)(**optimizer_config)
    metrics = config['metrics']

    # compile keras model
    model.compile(
        loss=loss,
        optimizer=optimizer,
        metrics=metrics)

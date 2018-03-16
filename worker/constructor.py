from keras import models
from keras import layers
from keras import optimizers
import h5py

import metadata
import storage


def create_model(architecture, shape):
    input = output = layers.Input(shape=shape)

    for layer in architecture['layers']:
        name = layer['name']
        config = layer['config']
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


def train_model_task(task_id):
    # load task metadata
    task = metadata.TaskMetadata.from_id(task_id)

    # load model metadata
    model_id = task.config['model']
    model_meta = metadata.ModelMetadata.from_id(model_id)

    # load architecture metadata
    architecture_id = model_meta.base.architecture
    architecture_meta = metadata.ArchitectureMetadata.from_id(architecture_id)
    architecture = architecture_meta.architecture

    # load dataset metadata
    dataset_id = task.config['dataset']
    dataset_meta = metadata.DatasetMetadata.from_id(dataset_id)
    dataset_name = dataset_meta.url

    # load dataset
    print('Open dataset:', dataset_name)
    dataset_path = storage.get_dataset_path(dataset_name)
    dataset = h5py.File(dataset_path)
    shape = dataset['x_train'].shape[1:]
    print('Input shape:', shape)

    # create keras model
    model = create_model(architecture, shape)
    model.summary()

    compile_model(model, task.config)

    # train
    batch_size = task.config.get('batch_size', 32)
    epochs = task.config.get('epochs', 1)
    x_train = dataset['x_train']
    y_train = dataset['y_train']
    x_test = dataset['x_test']
    y_test = dataset['y_test']

    # train keras model
    model.fit(
        x_train,
        y_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_data=(x_test, y_test),
        shuffle="batch")

    model_name = model_meta['url']
    model_path = storage.get_model_path(model_name)
    models.save_model(model, model_path)

import functools
import tempfile

import numpy
import h5py
import keras
from keras.datasets import cifar10


@functools.lru_cache(1)
def get_cifar10():
    _, file_path = tempfile.mkstemp('cifar10.hdf5')
    print('Temp dataset file:', file_path)
    cifar10_to_hdf5(file_path, part=0.0001)

    return file_path


def cifar10_to_hdf5(file_path, part=1.0):
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    num_classes = 10

    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    x_train /= 255
    x_test /= 255

    x = numpy.concatenate((x_train, x_test))
    y = numpy.concatenate((y_train, y_test))

    numpy.random.shuffle(x)
    numpy.random.shuffle(y)

    if part < 1.0:
        len = x.shape[0]
        border = int(len * part)

        x = x[:border]
        y = y[:border]

    with h5py.File(file_path, 'w') as f:
        f.create_dataset('x', data=x, compression='gzip')
        f.create_dataset('y', data=y, compression='gzip')

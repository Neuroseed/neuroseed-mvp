import os

import numpy
import h5py
import keras
from keras.preprocessing import sequence
from keras.datasets import reuters

from examples import utils


hdf5_file = 'reuters.hdf5'
batch_size = 32
num_classes = 46
path = 'reuters_word_index.json'


def create_dataset_meta():
    url = 'http://localhost:8080/api/v1/dataset'
    
    dataset_meta = {
        "is_public": True,
        "title": "Reuters newswire topics",
        "description": "Dataset of 11,228 newswires from Reuters, labeled over 46 topics. As with the IMDB dataset, each wire is encoded as a sequence of word indexes (same conventions).",
        "category": "classification"
    }

    r = utils.post(url, json=dataset_meta)
    print('Create dataset metadata: ', r.status_code, 'data:', r.text)

    if r.status_code == 200:
        return r.json()['id']
    
    raise RuntimeError('Status code', r.status_code, 'text:', r.text)


def reuters_to_hdf5(file_name):
    if os.path.exists(file_name):
        return

    (x_train, y_train), (x_test, y_test) = reuters.load_data(num_words=1000)
    word_index = reuters.get_word_index(path="reuters_word_index.json")
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    x_train = x_train.astype('object')
    x_test = x_test.astype('object')

    x = numpy.concatenate((x_train, x_test), axis=0)
    x = sequence.pad_sequences(x, maxlen=400)
    y = numpy.concatenate((y_train, y_test), axis=0)
#    y = sequence.pad_sequences(y, maxlen=400)

    with h5py.File(file_name, 'w') as f:
        f.create_dataset('x',data=x, compression='gzip')
        f.create_dataset('y',data=y, compression='gzip')
        dictionary = f.create_group('dictionary')
        for key in word_index:
            dictionary[key] = word_index[key]


if __name__ == '__main__':
    reuters_to_hdf5(hdf5_file)
    id = create_dataset_meta()
    utils.upload(id, hdf5_file)

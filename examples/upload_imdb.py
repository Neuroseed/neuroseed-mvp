import os

import numpy
import h5py
import keras
from keras.preprocessing import sequence
from keras.datasets import imdb

import utils


hdf5_file = 'imdb.hdf5'
batch_size = 32
num_classes = 2


def create_dataset_meta():
    url = 'http://localhost:8080/api/v1/dataset'

    dataset_meta = {
        "is_public": True,
        "title": "IMDB Movie reviews",
        "description": "Dataset of 25,000 movies reviews from IMDB, labeled by sentiment (positive/negative). Reviews have been preprocessed, and each review is encoded as a sequence of word indexes (integers). For convenience, words are indexed by overall frequency in the dataset, so that for instance the integer ""3"" encodes the 3rd most frequent word in the data. This allows for quick filtering operations such as: ""only consider the top 10,000 most common words, but eliminate the top 20 most common words"".",
        "category": "classification"
    }

    r = utils.post(url, json=dataset_meta)
    print('Create dataset metadata: ', r.status_code, 'data:', r.text)

    if r.status_code == 200:
        return r.json()['id']

    raise RuntimeError('Status code', r.status_code, 'text:', r.text)


def imdb_to_hdf5(file_name):
    if os.path.exists(file_name):
        return
    
    (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=20000)
    word_index = imdb.get_word_index(path="imdb_word_index.json")
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    x_train = x_train.astype('object')
    x_test = x_test.astype('object')

    x = numpy.concatenate((x_train, x_test), axis=0)
    x = sequence.pad_sequences(x, maxlen=80)
    y = numpy.concatenate((y_train, y_test), axis=0)
#    y = sequence.pad_sequences(y, maxlen=400)

    with h5py.File(file_name, 'w') as f:
        f.create_dataset('x',data=x, compression='gzip')
        f.create_dataset('y',data=y, compression='gzip')
        dictionary = f.create_group('dictionary')
        for key in word_index:
            dictionary[key] = word_index[key]


if __name__ == '__main__':
    imdb_to_hdf5(hdf5_file)
    id = create_dataset_meta()
    utils.upload(id, hdf5_file)

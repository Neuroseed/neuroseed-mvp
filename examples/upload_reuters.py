import numpy
import h5py
import keras
from keras.preprocessing import sequence
from keras.datasets import reuters

hdf5_file = 'reuters.hdf5'
batch_size = 32
num_classes = 46
path = 'reuters_word_index.json'


def imdb_to_hdf5(file_name):
    (x_train, y_train), (x_test, y_test) = reuters.load_data(num_words=10000, maxlen=500)
#    word_index = imdb.get_word_index(path="reuters_word_index.json")
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    x_train = x_train.astype('object')
    x_test = x_test.astype('object')
#    word_index = word_index.astype('string')

    x = numpy.concatenate((x_train, x_test), axis=0)
    x = sequence.pad_sequences(x, maxlen=400)
    y = numpy.concatenate((y_train, y_test), axis=0)
    y = sequence.pad_sequences(y, maxlen=400)
#    word_index = h5py.spetial_dtype(vlen=str)

    with h5py.File(file_name, 'w') as f:
        f.create_dataset('x',data=x, compression='gzip')
        f.create_dataset('y',data=y, compression='gzip')
#        word_index = f.create_group(('/dict'); for key in dict: word_index[key] = dict[key])

if __name__ == '__main__':
    imdb_to_hdf5(hdf5_file)

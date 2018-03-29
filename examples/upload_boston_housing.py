import os
import requests
import jwt
import numpy
import h5py
import utils
import keras
from keras.datasets import boston_housing


SECRET_KEY = 'secret'
payload = {'user_id': 'user-user-user'}

TOKEN = jwt.encode(payload, SECRET_KEY, algorithm='HS256',).decode('utf-8')

hdf5_file = 'boston_housing.hdf5'
batch_size = 32
num_classes = 51


def create_dataset_metadata():
    url = 'http://localhost:8080/api/v1/dataset'

    dataset_meta = {
        "is_public": True,
        "title": "Boston housing price",
        "description": "Dataset taken from the StatLib library which is maintained at Carnegie Mellon University. Samples contain 13 attributes of houses at different locations around the Boston suburbs in the late 1970s. Targets are the median values of the houses at a location (in k$).",
        "category": "regression"
    }

    headers = {
        'Authorization': 'Bearer {token}'.format(token=TOKEN)
    }
    r = requests.post(url, json=dataset_meta, headers=headers)
    print('Create dataset metadata: ', r.status_code, 'data:', r.text)

    if r.status_code == 200:
        return r.json()['id']

    raise RuntimeError('Status_code', r.status_code, r.text)


def boston_housing_to_hdf5(file_name):
    if os.path.exists(file_name):
        return
    
    (x_train, y_train), (x_test, y_test) = boston_housing.load_data()
    
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')
    
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)
    
    x_train = x_train.astype('float64')
    x_test = x_test.astype('float64')
    
    x = numpy.concatenate((x_train, x_test))
    y = numpy.concatenate((y_train, y_test))
    
    numpy.random.shuffle(x)
    numpy.random.shuffle(y)
    
    with h5py.File(file_name, 'w') as f:
        f.create_dataset('x',data=x, compression='gzip')
        f.create_dataset('y',data=y, compression='gzip')


if __name__ == '__main__':
    boston_housing_to_hdf5(hdf5_file)
    id = create_dataset_metadata()
    utils.upload(id, hdf5_file)


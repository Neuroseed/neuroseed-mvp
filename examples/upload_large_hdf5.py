import base64
import requests
import numpy
import h5py

SEND_FILE = 'tests/large_dataset.hdf5'
DATASET_ID = 'd1'
URL = 'http://localhost:8080/api/v1/dataset/{}'.format(DATASET_ID)


def create_hdf5(file_name):
    f = h5py.File(file_name, 'w')

    # float size 4 bytes
    n = 10**6
    dataset = f.create_dataset('dataset', (n,), dtype='f')

    dataset[...] = numpy.ones(n)

    f.close()


def upload(file_name):
    with open(file_name, 'rb') as f:
        raw = f.read()
        data = base64.b64encode(raw)

        headers = {
            'Content-Type': 'text/plain',
        }
        r = requests.post(
            URL, 
            data=data, 
            headers=headers)

        print('Status:', r.status_code, 'Resp:', r.text)


if __name__ == '__main__':
    create_hdf5(SEND_FILE)
    upload(SEND_FILE)


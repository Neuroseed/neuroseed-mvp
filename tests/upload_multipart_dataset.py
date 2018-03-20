import requests
import numpy
import h5py
import jwt
from requests_toolbelt.multipart import encoder

SECRET_KEY = 'secret'

payload = {
    'user_id': 'user-user-user',
}
TOKEN = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

SEND_FILE = 'tests/large_dataset.hdf5'
DATASET_ID = 'b54a6da7-7e87-473a-9d93-8f3e6f8a0864'
URL = 'http://localhost:8080/api/v1/dataset/{}'.format(DATASET_ID)


def create_hdf5(file_name):
    f = h5py.File(file_name, 'w')

    # float size 4 bytes
    n = 10**4
    dataset = f.create_dataset('dataset', (n,), dtype='f')

    dataset[...] = numpy.ones(n)

    f.close()


def upload(file_name):
    with open(file_name, 'rb') as f:
        form = encoder.MultipartEncoder({
            "file": (file_name, f, "text/plain")
        })
        print("Content-Type:", form.content_type)

        headers = {
            "Prefer": "respond-async",
            "Content-Type": form.content_type,
            'Authorization': 'Bearer {token}'.format(token=TOKEN)
        }

        resp = requests.post(URL, headers=headers, data=form, stream=True)

        print('Status code:', resp.status_code, 'resp.text:', resp.text)


if __name__ == '__main__':
    create_hdf5(SEND_FILE)
    upload(SEND_FILE)


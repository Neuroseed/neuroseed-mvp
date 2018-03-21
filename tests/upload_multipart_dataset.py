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


def create_hdf5(file_name):
    f = h5py.File(file_name, 'w')

    # float size 4 bytes
    n = 10**8
    dataset = f.create_dataset('dataset', (n,), dtype='f')

    dataset[...] = numpy.ones(n)

    f.close()


def create_dataset_metadata():
    url = 'http://localhost:8080/api/v1/dataset'

    dataset_meta = {
        "is_public": False,
        "title": "Test Dataset123",
        "description": "Test test",
        "category": "classification",
    }

    headers = {
        'Authorization': 'Bearer {token}'.format(token=TOKEN)
    }

    r = requests.post(url, json=dataset_meta, headers=headers)

    print('Create dataset metadata:', r.status_code, 'data:', r.text)

    if r.status_code == 200:
        return r.json()['id']


def upload(dataset_id, file_name):
    url = 'http://localhost:8080/api/v1/dataset/{}'.format(dataset_id)

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

        resp = requests.post(url, headers=headers, data=form, stream=True)

        print('Upload dataset:', resp.status_code, 'resp.text:', resp.text)


if __name__ == '__main__':
    create_hdf5(SEND_FILE)
    id = create_dataset_metadata()
    upload(id, SEND_FILE)


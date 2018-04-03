import os
import requests
import jwt
from requests_toolbelt.multipart import encoder

def get_auth_header():
    here = os.path.abspath(os.path.dirname(__file__))
    auth_key_file = os.path.join(here, '../config/auth.key')
    # print('Load auth key from:', auth_key_file)

    with open(auth_key_file) as f:
        secret_key = f.read().strip()

    payload = {
        'user_id': 'u1',
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')

    return {
        'Authorization': 'Bearer {token}'.format(token=token)
    }


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
        }
            
        resp = post(url, headers=headers, data=form, stream=True)
    print('Upload dataset:', resp.status_code, 'resp.text:', resp.text)


def get(*args, **kwargs):
    headers = kwargs.setdefault('headers', {})
    headers.update(get_auth_header())

    return requests.get(*args, **kwargs)


def post(*args, **kwargs):
    headers = kwargs.setdefault('headers', {})
    headers.update(get_auth_header())

    return requests.post(*args, **kwargs)

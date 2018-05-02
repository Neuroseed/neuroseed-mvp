import os
import functools
import requests
import jwt
from requests_toolbelt.multipart import encoder

DEFAULT_USER_ID = 'u1'


def get_auth_token(user_id=None):
    here = os.path.abspath(os.path.dirname(__file__))
    auth_key_file = os.path.join(here, '../config/auth.key')
    # print('Load auth key from:', auth_key_file)

    with open(auth_key_file) as f:
        secret_key = f.read().strip()

    payload = {
        'user_id': user_id or DEFAULT_USER_ID,
    }

    return jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')


def get_auth_header(user_id=None):
    token = get_auth_token(user_id or DEFAULT_USER_ID)

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


def method(name, *args, **kwargs):
    headers = kwargs.setdefault('headers', {})

    user_id = kwargs.pop('user_id', None)
    auth_headers = get_auth_header(user_id)
    headers.update(auth_headers)

    http_method = getattr(requests, name)

    return http_method(*args, **kwargs)


get = functools.partial(method, 'get')
post = functools.partial(method, 'post')
delete = functools.partial(method, 'delete')
patch = functools.partial(method, 'patch')

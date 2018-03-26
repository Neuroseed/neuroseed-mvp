import os
import requests
import jwt


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


def get(*args, **kwargs):
    headers = kwargs.setdefault('headers', {})
    headers.update(get_auth_header())

    return requests.get(*args, **kwargs)


def post(*args, **kwargs):
    headers = kwargs.setdefault('headers', {})
    headers.update(get_auth_header())

    return requests.post(*args, **kwargs)

import requests
import jwt

SECRET_KEY = 'secret'

payload = {
    'user_id': 'user-user-user',
}
TOKEN = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

ID = '9271a346e0e048f8adf17fdd09752951'
url = 'http://localhost:8080/api/v1/model/{id}/train'.format(id=ID)

config = {
    "dataset": "907dced87deb42d3b88ed8a34f94f920",
    "optimizer": "sgt",
    "loss": "mean_square_loss"
}

headers = {
    'Authorization': 'Bearer {token}'.format(token=TOKEN)
}

r = requests.post(url, json=config, headers=headers)

print('status:', r.status_code, 'data:', r.text)


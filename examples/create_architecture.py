import requests
import jwt

SECRET_KEY = 'secret'

payload = {
    'user_id': 'user-user-user',
}
TOKEN = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

url = 'http://localhost:8080/api/v1/architecture'

architecture = {
    "layers": [
        "input",
        "conv2d",
        "maxpooling2d",
        "conv2d",
        "flatten",
        "dense"
    ]
}

data = {
    "id": "arch1",
    "is_public": False,
    "title": "title",
    "description": "description",
    "category": "adfad",
    "architecture": architecture
}

headers = {
    'Authorization': 'Bearer {token}'.format(token=TOKEN)
}

r = requests.post(url, json=data, headers=headers)

print('status:', r.status_code, 'data:', r.text)


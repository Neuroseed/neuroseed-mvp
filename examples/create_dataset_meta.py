import requests
import jwt

SECRET_KEY = 'secret'

payload = {
    'user_id': 'user-user-user',
}
TOKEN = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

url = 'http://localhost:8080/api/v1/dataset'

dataset_meta={
    "is_public": False,
    "title": "Test Dataset123",
    "description": "Test test",
    "category": "classification",
}

headers = {
    'Authorization': 'Bearer {token}'.format(token=TOKEN)
}

r = requests.post(url, json=dataset_meta, headers=headers)

print('status:', r.status_code, 'data:', r.text)


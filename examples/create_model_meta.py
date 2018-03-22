import requests
import jwt

SECRET_KEY = 'secret'

payload = {
    'user_id': 'user-user-user',
}
TOKEN = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

url = 'http://localhost:8080/api/v1/model'

model = {
    "is_public": False,
    "title": "Test Model",
    "description": "Test test test",
    "category": "classification",
    "labels": ["a", "b", "c"],
    "architecture": "arch-id",
    "dataset": "d1"
}
headers = {
    'Authorization': 'Bearer {token}'.format(token=TOKEN)
}

r = requests.post(url, json=model, headers=headers)

print('status:', r.status_code, 'data:', r.text)


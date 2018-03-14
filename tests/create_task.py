import requests
import jwt

SECRET_KEY = 'secret'

payload = {
    'user_id': 'user-user-user',
}
TOKEN = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

url = 'http://localhost:8080/api/v1/task'

task = {
    "command": "predict",
    "config": {
        "dataset": "d1",
        "accuracy": 0.7,
        "epochs": 10
    }
}

headers = {
    'Authorization': 'Bearer {token}'.format(token=TOKEN)
}

r = requests.post(url, json=task, headers=headers)

print('status:', r.status_code, 'data:', r.text)


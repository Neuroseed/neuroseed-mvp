import requests

url = 'http://localhost:8080/api/v1/task'

task = {
    "command": "predict",
    "config": {
        "dataset": "d1",
        "accuracy": 0.7,
        "epochs": 10
    }
}

r = requests.post(url, json=task)

print('status:', r.status_code, 'data:', r.text)


import requests

url = 'http://localhost:8080/api/v1/dataset'

dataset_meta={
    "is_public": False,
    "title": "Test Dataset123",
    "description": "Test test",
    "category": "classification",
}

r = requests.post(url, json=dataset_meta)

print('status:', r.status_code, 'data:', r.text)


import requests

ID = '483167de-94fc-4adf-a8fd-71487d512207'
url = 'http://localhost:8080/api/v1/model/{id}/train'.format(id=ID)

model={
    "is_public": False,
    "meta":{
        "title": "Test Model",
        "description": "Test test test",
        "category": "classification",
        "labels": ["a", "b", "c"],
        "architecture": "arch-id",
        "dataset": "d1"
    }
}

r = requests.post(url, json=model)

print('status:', r.status_code, 'data:', r.text)


import requests

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

r = requests.post(url, json=data)

print('status:', r.status_code, 'data:', r.text)


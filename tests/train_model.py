import requests

ID = '483167de-94fc-4adf-a8fd-71487d512207'
url = 'http://localhost:8080/api/v1/model/{id}/train'.format(id=ID)

config = {
    "dataset": "907dced87deb42d3b88ed8a34f94f920"
}

r = requests.post(url, json=config)

print('status:', r.status_code, 'data:', r.text)


import requests

ID = '02c92d6f2c924a8395d9b9034e264bd6'
url = 'http://localhost:8080/api/v1/model/{id}/train'.format(id=ID)

config = {
    "dataset": "907dced87deb42d3b88ed8a34f94f920",
    "optimizer": "sgt",
    "loss": "mean_square_loss"
}

r = requests.post(url, json=config)

print('status:', r.status_code, 'data:', r.text)


import time
import utils


def create_dataset():
    url = 'http://localhost:8080/api/v1/dataset'

    json = {
        "is_public": True,
        "title": "Test Dataset {id}".format(id=int(time.time()) % 1000),
        "description": "Test test",
        "category": "classification",
    }

    resp = utils.post(url, json=json)

    print('status:', resp.status_code, 'data:', resp.text)

    if resp.status_code == 200:
        return resp.json()['id']


if __name__ == '__main__':
    create_dataset()

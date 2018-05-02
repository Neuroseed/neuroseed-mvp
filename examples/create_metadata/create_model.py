import time

from examples import utils
import create_architecture
import create_dataset


def create_model_metadata():
    aid = create_architecture.create_architecture()
    did = create_dataset.create_dataset()

    url = 'http://localhost:8080/api/v1/model'

    model = {
        "is_public": True,
        "title": "Test Model {id}".format(id=int(time.time()) % 1000),
        "description": "Test test test",
        "labels": ["a", "b", "c"],
        "architecture": aid,
        "dataset": did
    }

    resp = utils.post(url, json=model)

    print('status:', resp.status_code, 'data:', resp.text)

    if resp.status_code == 200:
        return resp.json()['id']


if __name__ == '__main__':
    create_model_metadata()

from examples import utils


def create_task():
    url = 'http://localhost:8080/api/v1/task'

    task = {
        "command": "model.train",
        "config": {
            "dataset": "d1",
            "accuracy": 0.7,
            "epochs": 10
        }
    }

    resp = utils.post(url, json=task)

    print('status:', resp.status_code, 'data:', resp.text)

    if resp.status_code == 200:
        return resp.json()['id']


if __name__ == '__main__':
    create_task()

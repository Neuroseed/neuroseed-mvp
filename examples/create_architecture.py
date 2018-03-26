import utils


def create_architecture():
    url = 'http://localhost:8080/api/v1/architecture'

    architecture = {
        "layers": [
            {"name": "input"},
            {"name": "conv2d"},
            {"name": "maxpooling2d"},
            {"name": "conv2d"},
            {"name": "flatten"},
            {"name": "dense"}
        ]
    }

    data = {
        "id": "arch1",
        "is_public": True,
        "title": "title",
        "description": "description",
        "architecture": architecture
    }

    resp = utils.post(url, json=data)

    print('status:', resp.status_code, 'data:', resp.text)

    if resp.status_code == 200:
        return resp.json()['id']


if __name__ == '__main__':
    create_architecture()

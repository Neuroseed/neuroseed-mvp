from examples import utils


def create_architecture():
    url = 'http://localhost:8080/api/v1/architecture'

    architecture = {
        "layers": [
            {
                "name": "Embedding",
                "config": {
                    "input_dim": 20000,
                    "output_dim": 128
                }
            },
            {
                "name": "LSTM",
                "config": {
                    "units": 128,
                   "dropout": 0.2,
                   "recurrent_dropout": 0.2
                }
            },
            {
               "name": "Dense",
               "config": {
                   "units": 2,
                   "activation": "sigmoid"
               }
           }
        ]
    }

    data = {
        "is_public": True,
        "title": "LSTM architecture for imdb dataset",
        "architecture": architecture
    }

    resp = utils.post(url, json=data)

    if resp.status_code == 200:
        print('Create architecture status:', resp.status_code, 'data:', resp.text)
        return resp.json()['id']

    raise RuntimeError('status: {code} data: {text}'.format(code=resp.status_code, text=resp.text))


def create_model(architecture_id, dataset_id):
    url = 'http://localhost:8080/api/v1/model'

    model = {
        "is_public": True,
        "title": "Classification CNN on imdb",
        "architecture": architecture_id,
        "dataset": dataset_id
    }

    resp = utils.post(url, json=model)

    if resp.status_code == 200:
        print('Create model status:', resp.status_code, 'data:', resp.text)
        return resp.json()['id']

    raise RuntimeError('status: {code} data: {text}'.format(code=resp.status_code, text=resp.text))


def train_cnn_cifar10(model_id):
    url = 'http://localhost:8080/api/v1/model/{id}/train'.format(id=model_id)

    config = {
        "epochs": 1,
        "optimizer": {
            "name": "Adam"
        },
        "loss": "binary_crossentropy"
    }

    resp = utils.post(url, json=config)

    if resp.status_code == 200:
        print('Train model status:', resp.status_code, 'data:', resp.text)
        return resp.json()['id']

    raise RuntimeError('status: {code} data: {text}'.format(code=resp.status_code, text=resp.text))


if __name__ == '__main__':
    architecture_id = create_architecture()
    dataset_id = input('Dataset ID: ')

    model_id = create_model(architecture_id, dataset_id)

    task_id = train_cnn_cifar10(model_id)

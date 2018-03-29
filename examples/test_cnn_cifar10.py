import utils


def test_cnn_cifar10(dataset_id, model_id):
    url = 'http://localhost:8080/api/v1/model/{id}/test'.format(id=model_id)
    json = {
        'dataset': dataset_id
    }

    resp = utils.post(url, json=json)

    if resp.status_code == 200:
        print('Test model status:', resp.status_code, 'data:', resp.text)
        return resp.json()['id']

    raise RuntimeError('status: {code} data: {text}'.format(code=resp.status_code, text=resp.text))


if __name__ == '__main__':
    dataset_id = input('Dataset ID: ')
    model_id = input('Model ID: ')

    test_cnn_cifar10(dataset_id, model_id)

from examples import utils


def train_model():
    ID = '9271a346e0e048f8adf17fdd09752951'
    url = 'http://localhost:8080/api/v1/model/{id}/train'.format(id=ID)

    config = {
        "dataset": "907dced87deb42d3b88ed8a34f94f920",
        "optimizer": "sgt",
        "loss": "mean_square_loss"
    }

    resp = utils.post(url, json=config)

    print('status:', resp.status_code, 'data:', resp.text)

    if resp.status_code == 200:
        return resp.json()['id']


if __name__ == '__main__':
    train_model()

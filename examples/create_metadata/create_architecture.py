from examples import utils


def create_architecture():
    url = 'http://localhost:8080/api/v1/architecture'

    architecture = {
        "layers": [
               {
                   "name": "Dense",
                   "config": {
                       "units": 123,
                       "activation": "asdsd",
                       "use_bias": True,
                       "kernel_initializer": "asdsrq",
                       "bias_initializer": "asdasd",
                       "kernel_regularizer": "adasdq1",
                       "bias_regularizer": "112312",
                       "activity_regularizer": "35654wd",
                       "kernel_constraint": "ad123",
                       "bias_constraint": "ad1356"
                   }
                },
               {"name": "Dropout"},
               {
                   "name": "Conv2D",
                   "config": {
                       "filters": 123,
                       "kernel_size": [1, 2, 3],
                       "strides": [1,2],
                       "padding": "in my ass",
                       "dilation_rate": [1,2],
                       "activation": "asda",
                       "use_bias": True,
                       "kernel_initializer": "asdsrq",
                       "bias_initializer": "asdasd",
                       "kernel_regularizer": "adasdq1",
                       "bias_regularizer": "112312",
                       "activity_regularizer": "35654wd",
                       "kernel_constraint": "ad123",
                       "bias_constraint": "ad1356"
                   }
                },
               {"name": "Maxpooling2d"}
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

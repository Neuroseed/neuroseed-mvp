import base64
import requests

SEND_FILE = 'tests/upload_datasets.py'
DATASET_ID = 'd1'
URL = 'http://localhost:8080/api/v1/dataset/{}'.format(DATASET_ID)


def upload():
    with open(SEND_FILE, 'rb') as f:
        raw = f.read()
        data = base64.b64encode(raw)

        headers = {
            'Content-Type': 'text/plain',
        }
        r = requests.post(
            URL, 
            data=data, 
            headers=headers)

        print('Status:', r.status_code, 'Resp:', r.text)


if __name__ == '__main__':
    upload()


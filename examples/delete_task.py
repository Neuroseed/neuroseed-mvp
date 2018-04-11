import utils


def delete_task(task_id):
    url = 'http://localhost:8080/api/v1/task/{id}'.format(id=task_id)

    resp = utils.delete(url)

    if resp.status_code == 200:
        print('Delete task status:', resp.status_code, 'data:', resp.text)
        return

    raise RuntimeError('status: {code} data: {text}'.format(code=resp.status_code, text=resp.text))


if __name__ == '__main__':
    task_id = input('Task ID: ')

    delete_task(task_id)
    print('Task stopped.')

import time
from celery import states

import metadata
from ..app import app


@app.task(bind=True, name='model.train')
def train_model(self):
    task_id = self.request.id

    # TODO: replace code by shorter one
    try:
        task = metadata.Task.objects.get({'_id': task_id})
    except metadata.Task.DoesNotExist:
        self.update_state(state=states.FAILURE)
        return

    # TODO: replace code by shorter one
    try:
        model_id = task.config['model']
        model = metadata.Model.objects.get({'_id': model_id})
    except metadata.Model.DoesNotExist:
        self.update_state(state=states.FAILURE)
        return
    except KeyError as err:
        print('no model')
        self.update_state(state=states.FAILURE)
        return

    # TODO: replace code by shorter one
    try:
        dataset_id = task.config['dataset']
        dataset = metadata.Dataset.objects.get({'_id': dataset_id})
    except metadata.errors.DoesNotExist:
        self.update_state(state=states.FAILURE)
        return
    except KeyError as err:
        print('no dataset')
        self.update_state(state=states.FAILURE)
        return

    print('Task in mongo: {}'.format(task.to_son()))

    # TODO: compress code to one line
    self.update_state(state=states.STARTED)
    task.status = metadata.task.STARTED
    task.save()
    model.status = metadata.model.TRAINING
    model.save()
    print('Start train task: {}'.format(task_id))

    time.sleep(10)  # TODO: train here

    # TODO: compress code to one line
    self.update_state(state=states.SUCCESS)
    task.status = metadata.task.SUCCESS
    task.save()
    model.status = metadata.model.READY
    model.save()
    print('End train task: {}'.format(task_id))

    return {'id': task_id}

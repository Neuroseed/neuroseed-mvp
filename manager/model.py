import functools

from metadata.model import *
from . import task
from . import utils


def create_model_task(command, model, config, context):
    model = utils.prepare_model(model)

    config["model"] = model.id

    task_ = task.create_task(command, config, context)

    return task_


train_model = functools.partial(create_model_task, 'model.train')
test_model = functools.partial(create_model_task, 'model.test')
predict_model = functools.partial(create_model_task, 'model.predict')

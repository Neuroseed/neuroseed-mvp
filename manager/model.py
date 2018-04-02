import metadata
from metadata import ModelMetadata
from . import utils


def create_model_task(command, config, model_id, owner):
    try:
        model = ModelMetadata.from_id(id=model_id)
    except metadata.DoesNotExist as err:
        raise

    config["model"] = model_id

    id = utils.create_task(command, config, owner)

    return id


def train_model(config, model_id, owner):
    return create_model_task('model.train', config, model_id, owner)


def test_model(config, model_id, owner):
    return create_model_task('model.test', config, model_id, owner)


def predict_model(config, model_id, owner):
    return create_model_task('model.predict', config, model_id, owner)

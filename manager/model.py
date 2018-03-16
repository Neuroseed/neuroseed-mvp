import metadata
from . import utils
from webapi import errors


class Model(metadata.ModelMetadata):
    def __init__(self, *args, **kwargs):
        flatten = None
        if 'flatten' in kwargs:
            flatten = kwargs['flatten']
            del kwargs['flatten']

        super().__init__(*args, **kwargs)

        if flatten:
            self.from_flatten(flatten)

        self.url = self.id

    def flatten(self):
        """Return model in flatten representation"""

        meta = self.to_mongo().to_dict()

        if '_id' in meta:
            meta['id'] = meta['_id']
            del meta['_id']

        meta.update(meta['base'])
        del meta['base']
        del meta['_cls']

        return meta

    to_dict = flatten

    def from_flatten(self, meta):
        """Restore model metadata from flatten representation"""

        for name in self._fields:
            if not name is 'base' and name in meta:
                setattr(self, name, meta[name])

        for name in self.base._fields:
            if name in meta:
                setattr(self.base, name, meta[name])

    from_dict = from_flatten


def get_models():
    models_meta = Model.objects.all()
    ids = [meta.id for meta in models_meta]

    return ids


def create_model_task(command, config, model_id, owner):
    try:
        model = Model.from_id(model_id)
    except metadata.DoesNotExist as err:
        raise

    config["model"] = model_id

    id = utils.create_task(command, config, owner)

    return id


def train_model(config, model_id, owner):
    return create_model_task('model.train', config, model_id, owner)


def test_model(config, model_id):
    return create_model_task('model.test', config, model_id)


def predict_model(config, model_id):
    return create_model_task('model.predict', config, model_id)

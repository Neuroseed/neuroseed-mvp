import logging

import falcon
import metadata

__all__ = [
    'ModelsResource',
    'ModelsFullResource',
    'ModelsNumberResource'
]

logger = logging.getLogger(__name__)


class ModelsResource:
    def on_get(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        models = metadata.ModelMetadata.objects(is_public=True)
        ids = [meta.id for meta in models]

        if user_id:
            models = metadata.ModelMetadata.objects(is_public=False, base__owner=user_id)
            ids = [meta.id for meta in models] + ids

        resp.status = falcon.HTTP_200
        resp.media = {
            'ids': ids  # response schema v0.2.1
        }


class ModelsFullResource:
    def on_get(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        models = metadata.ModelMetadata.objects(is_public=True)
        models_meta = self.get_models_meta(models)

        if user_id:
            models = metadata.ModelMetadata.objects(is_public=False, base__owner=user_id)
            models_meta = self.get_models_meta(models) + models_meta

        from_ = int(req.params.get('from', 0))
        number = int(req.params.get('number', 99999))
        if from_ < len(models_meta):
            models_meta = models_meta[from_: from_ + number]

        resp.status = falcon.HTTP_200
        resp.media = {
            'models': models_meta  # response schema v0.2.2
        }

    @staticmethod
    def get_models_meta(models):
        models_meta = []

        for model in models:
            model_meta = {
                'id': model.id,
                'is_public': model.is_public,
                'hash': model.hash,
                'owner': model.base.owner,
                'size': model.base.size,
                'date': model.base.date,
                'title': model.base.title,
                'description': model.base.description,
                'category': model.base.category,
                'labels': model.base.labels,
                'accuracy': model.base.accuracy,
                'dataset': model.base.dataset
            }
            models_meta.append(model_meta)

        return models_meta


class ModelsNumberResource:
    def on_get(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        number = metadata.ModelMetadata.objects(is_public=True).count()

        if user_id:
            number += metadata.ModelMetadata.objects(is_public=False, base__owner=user_id).count()

        resp.status = falcon.HTTP_200
        resp.media = number

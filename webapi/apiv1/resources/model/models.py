import logging

from mongoengine.queryset.visitor import Q
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

        context = {'user_id': user_id}
        models = metadata.get_models(context)
        ids = [meta.id for meta in models]

        resp.status = falcon.HTTP_200
        resp.media = {
            'ids': ids  # response schema v0.2.1
        }


class ModelsFullResource:
    def on_get(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        from_ = int(req.params.get('from', 0))

        if from_ < 0:
            raise falcon.HTTPBadRequest(
                title="Bad Request",
                description="From must be greater than 0"
            )

        number = int(req.params.get('number', 99999))

        if number < 0:
            raise falcon.HTTPBadRequest(
                title="Bad Request",
                description="Number must be greater than 0"
            )

        context = {'user_id': user_id}
        filter = {'from': from_, 'number': number}
        models = metadata.get_models(context, filter)
        models_meta = self.get_models_meta(models)

        resp.status = falcon.HTTP_200
        resp.media = {
            'models': models_meta  # response schema v0.2.2
        }

    @staticmethod
    def get_models_meta(models):
        models_meta = []

        for model in models:
            model_meta_dict = model.to_dict()
            result_keys = ['id', 'status', 'is_public', 'hash', 'owner', 'size', 'date', 'title', 'description',
                           'category', 'labels', 'metrics', 'architecture', 'dataset']
            model_meta = {key: model_meta_dict[key] for key in result_keys if key in model_meta_dict}
            models_meta.append(model_meta)

        return models_meta


class ModelsNumberResource:
    def on_get(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        context = {'user_id': user_id}
        number = metadata.get_models(context).count()

        resp.status = falcon.HTTP_200
        resp.media = number

import logging

from mongoengine.queryset.visitor import Q
import falcon
import metadata

__all__ = [
    'DatasetsResource',
    'DatasetsFullResource',
    'DatasetsNumberResource'
]

logger = logging.getLogger(__name__)


class DatasetsResource:
    def on_get(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        datasets = metadata.DatasetMetadata.objects(is_public=True)
        ids = [meta.id for meta in datasets]

        if user_id:
            datasets = metadata.DatasetMetadata.objects(is_public=False, base__owner=user_id)
            ids = [meta.id for meta in datasets] + ids

        resp.status = falcon.HTTP_200
        resp.media = {
            'ids': ids  # response schema v0.2.1
        }


class DatasetsFullResource:
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

        query = Q(is_public=True)

        if user_id:
            query = query | (Q(is_public=False) & Q(base__owner=user_id))

        datasets = metadata.DatasetMetadata.objects(query).skip(from_).limit(number)
        datasets_meta = self.get_datasets_meta(datasets)

        resp.status = falcon.HTTP_200
        resp.media = {
            'datasets': datasets_meta  # response schema v0.2.2
        }

    @staticmethod
    def get_datasets_meta(datasets):
        datasets_meta = []

        for dataset in datasets:
            dataset_meta_dict = dataset.to_dict()
            result_keys = ['id', 'status', 'is_public', 'title', 'description', 'category', 'labels']
            dataset_meta = {key: dataset_meta_dict[key] for key in result_keys if key in dataset_meta_dict}
            datasets_meta.append(dataset_meta)

        return datasets_meta


class DatasetsNumberResource:
    def on_get(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        number = metadata.DatasetMetadata.objects(is_public=True).count()

        if user_id:
            number += metadata.DatasetMetadata.objects(is_public=False, base__owner=user_id).count()

        resp.status = falcon.HTTP_200
        resp.media = number

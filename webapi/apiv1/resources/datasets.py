import logging

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

        datasets = metadata.DatasetMetadata.objects(is_public=True)
        datasets_meta = self.get_datasets_meta(datasets)

        if user_id:
            datasets = metadata.DatasetMetadata.objects(is_public=False, base__owner=user_id)
            datasets_meta = self.get_datasets_meta(datasets) + datasets_meta

        from_ = int(req.params.get('from', 0))
        number = int(req.params.get('number', 99999))
        print('params:', from_, number)
        if from_ < len(datasets_meta):
            datasets_meta = datasets_meta[from_: from_ + number]

        resp.status = falcon.HTTP_200
        resp.media = {
            'datasets': datasets_meta  # response schema v0.2.2
        }

    @staticmethod
    def get_datasets_meta(datasets):
        datasets_meta = []

        for dataset in datasets:
            dataset_meta = {
                'id': dataset.id,
                'is_public': dataset.is_public,
                'title': dataset.base.title,
                'description': dataset.base.description,
                'category': dataset.base.category,
                'labels': dataset.base.labels
            }
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

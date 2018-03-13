import uuid
import metadata


def get_dataset_meta(id):
    try:
        dataset = metadata.DatasetMetadata.objects(id=id)
    except metadata.DoesNotExist:
        dataset = None

    if dataset:
        meta = {
            'id': dataset.id,
            'is_public': dataset.is_public,
            'title': dataset.base.title,
            'description': dataset.base.description,
            'category': dataset.base.category,
            'labels': dataset.base.labels
        }
        return meta
    else:
        raise metadata.DoesNotExist('Dataset does not exist')


def create_dataset(meta):
    base = meta.copy()
    del base['is_public']
    document = {
        'is_public': meta['is_public'],
        'base': base
    }
    dataset = metadata.DatasetMetadata(**document)
    dataset.id = str(uuid.uuid4())
    dataset.url = dataset.id
    dataset.base.owner = '0'
    dataset.save()

    return dataset.id


def get_datasets():
    datasets = metadata.Dataset.objects.all()
    ids = [meta.id for meta in datasets]

    return ids

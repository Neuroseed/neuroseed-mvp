import uuid
import metadata


def get_architecture_meta(id):
    try:
        architecture = metadata.ArchitectureMetadata.objects(id=id)
    except metadata.DoesNotExist:
        architecture = None

    if architecture:
        meta = {
            'id': architecture.id,
            'is_public': architecture.is_public,
            'owner': architecture.owner,
            'title': architecture.title,
            'description': architecture.description,
            'category': architecture.category,
            'architecture': architecture.architecture
        }
        return meta
    else:
        metadata.DoesNotExist('Architecture does not exist')


def create_architecture(meta):
    id = meta.get('id', None) or str(uuid.uuid4())

    architecture = metadata.ArchitectureMetadata(**meta)
    architecture.id = id
    architecture.owner = '0'
    architecture.save()

    return id


def get_architectures():
    architectures = metadata.ArchitectureMetadata.objects.all()
    ids = [arch.id for arch in architectures]

    return ids

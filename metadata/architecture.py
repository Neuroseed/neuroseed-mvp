from pymodm import MongoModel, fields

__all__ = [
    'Architecture'
]


class Architecture(MongoModel):
    id = fields.CharField(primary_key=True)
    is_public = fields.BooleanField(default=False)
    owner = fields.CharField(required=True)
    title = fields.CharField(required=True)
    description = fields.CharField()
    category = fields.CharField()
    architecture = fields.DictField(required=True)

    class Meta:
        connection_alias = 'metadata'
        collection_name = 'architectures'


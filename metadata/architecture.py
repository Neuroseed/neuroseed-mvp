from pymodm import MongoModel, fields

__all__ = [
    'Architecture'
]

class Architecture(MongoModel):
    id = fields.CharField(primary_key=True)
    is_public = fields.BooleanField(default=False)
    owner = fields.CharField()
    date = fields.TimestampField()
    title = fields.CharField()
    description = fields.CharField()
    category = fields.CharField()
    architecture = fields.DictField()

    class Meta:
        connection_alias = 'metadata'
        collection_name = 'architectures'


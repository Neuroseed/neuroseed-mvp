
class MetadataMixin:
    @classmethod
    def from_id(cls, id, **kwargs):
        return cls.objects.get(id=id, class_check=False, **kwargs)

    @classmethod
    def all_from_id(cls, **kwargs):
        return cls.objects(class_check=False, **kwargs)

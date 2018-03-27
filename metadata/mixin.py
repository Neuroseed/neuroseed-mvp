
class MetadataMixin:
    @classmethod
    def from_id(cls, *args, **kwargs):
        return cls.objects.get(*args, class_check=False, **kwargs)

    @classmethod
    def all_from_id(cls, *args, **kwargs):
        return cls.objects(*args, class_check=False, **kwargs)

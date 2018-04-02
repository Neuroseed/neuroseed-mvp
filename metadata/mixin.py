import contextlib


class MetadataMixin:
    @classmethod
    def from_id(cls, *args, **kwargs):
        return cls.objects.get(*args, class_check=False, **kwargs)

    @classmethod
    def all_from_id(cls, *args, **kwargs):
        return cls.objects(*args, class_check=False, **kwargs)

    @contextlib.contextmanager
    def save_context(self):
        """Save all changes in metadata does in context manager"""

        yield self  # wait for exit from context

        self.save()

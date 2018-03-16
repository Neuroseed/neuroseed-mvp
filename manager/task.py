import uuid

import metadata


class Task(metadata.TaskMetadata):
    def to_dict(self):
        meta = self.to_mongo().to_dict()

        if '_id' in meta:
            meta['id'] = meta['_id']
            del meta['_id']

        del meta['_cls']

        return meta

    def from_dict(self, meta):
        for name in self._fields:
            setattr(self, name, meta[name])


def get_tasks_ids():
    tasks = Task.objects.all()
    ids = [task.id for task in tasks]

    return ids

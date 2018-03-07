import falcon
import metadata

__all__ = [
    'ArchitecturesResource'
]


class ArchitecturesResource:
    def on_get(self, req, resp):
        architectures = metadata.Architecture.objects.all()

        architectures_ids = [arch.id for arch in architectures]

        resp.status = falcon.HTTP_200
        resp.media = {
            'success': True,
            'architectures': architectures_ids
        }


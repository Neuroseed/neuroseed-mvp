import falcon
import metadata

__all__ = [
    'ArchitecturesResource'
]


class ArchitecturesResource:
    def on_get(self, req, resp):
        architectures = metadata.ArchitectureMetadata.objects.all()

        ids = [arch.id for arch in architectures]

        resp.status = falcon.HTTP_200
        resp.media = {
            'ids': ids  # response schema v0.2.1
        }


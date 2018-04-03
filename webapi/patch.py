import logging
import hashlib

from falcon.request_helpers import BoundedStream

logger = logging.getLogger(__name__)


# TODO: FIX FALCON BUG AND DELETE THIS MONKEY PATH !!!
def _read(self, size, target):
    """Helper function for proxing reads to the underlying stream.
    Args:
        size (int): Maximum number of bytes to read. Will be
            coerced, if None or -1, to the number of remaining bytes
            in the stream. Will likewise be coerced if greater than
            the number of remaining bytes, to avoid making a
            blocking call to the wrapped stream.
        target (callable): Once `size` has been fixed up, this function
            will be called to actually do the work.
    Returns:
        bytes: Data read from the stream, as returned by `target`.
    """

    # NOTE(kgriffs): Default to reading all remaining bytes if the
    # size is not specified or is out of bounds. This behaves
    # similarly to the IO streams passed in by non-wsgiref servers.
    if (size is None or size == -1 or size > self._bytes_remaining):
        size = self._bytes_remaining

    raw = target(size)
    self._bytes_remaining -= len(raw)
    return raw

code_hash = hashlib.sha256(BoundedStream._read.__code__.co_code).hexdigest()
old_code_hash = 'f01e0ef4b334be2ac60c8740a675223da618257bb0ae25a7a29bfbdd812be3a7'
if code_hash != old_code_hash:
    logger.warning('Falcon fix BoundedStream.readline bug')

BoundedStream._read = _read
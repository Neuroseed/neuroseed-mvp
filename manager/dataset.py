import logging
import os
import time
import hashlib

import metadata
import storage
from metadata.dataset import *

logger = logging.getLogger(__file__)

CHUNK_SIZE_BYTES = 4096


def file_to_hash(file_path):
    hash = hashlib.sha256()

    with open(file_path, 'rb') as f:
        while True:
            raw = f.read(1024)

            if not raw:
                break

            hash.update(raw)

    return hash.hexdigest()


def save_dataset(meta, fileio):
    url = meta.url
    dataset_path = storage.get_dataset_path(url)

    # save dataset
    with storage.open_dataset(url, mode='wb', raw=True) as f:
        logger.debug('Save dataset to file {path}'.format(path=dataset_path))

        while True:
            chunk = fileio.read(CHUNK_SIZE_BYTES)
            if not chunk:
                break
            f.write(chunk)

    # validate hdf5
    try:
        with storage.open_dataset(url, mode='r') as f:
            _ = f['x']
            _ = f['y']
    except OSError as err:
        os.remove(dataset_path)
        raise
    except KeyError as err:
        os.remove(dataset_path)
        raise

    with meta.save_context():
        # save date
        meta.base.date = int(time.time())

        # save dataset size
        statinfo = os.stat(dataset_path)
        file_size = statinfo.st_size
        meta.base.size = int(file_size)

        # save dataset hash
        meta.base.hash = file_to_hash(dataset_path)

        # change status
        meta.status = metadata.dataset.RECEIVED

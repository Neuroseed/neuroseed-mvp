import logging
import logging.handlers
import sys
import os


def init_logging():
    def excepthook(type, value, traceback):
        logging.critical('Uncaught exception',
                         exc_info=(type, value, traceback))

        sys.__excepthook__(type, value, traceback)

        sys.exit(1)

    sys.excepthook = excepthook

    if not os.path.isdir('logs'):
        os.mkdir('logs')

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    file_handler = logging.handlers.RotatingFileHandler('logs/log-web-api.txt', mode='a', maxBytes=2**20, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    logging.warning('Start logging')

import logging

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)s %(funcName)s %(message)s'
)


def make_logger(name, loglevel):
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    return logger

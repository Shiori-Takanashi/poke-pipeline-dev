# util/logger.py
import logging, sys


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
        logger.addHandler(h)
    logger.setLevel(logging.INFO)
    return logger

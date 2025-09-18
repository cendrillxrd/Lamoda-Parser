import os
import logging
import sys

from config import DEBUG, HOME_DIR


def log_message(file_name: str, message: str, log_level: str, *args, **kwargs):
    log_dir = HOME_DIR / 'logs'
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.Logger('lis-logger', log_level)
    handler = logging.FileHandler(f'{log_dir}/{file_name}.log')
    handler.setFormatter(logging.Formatter("%(asctime)s %(message)s", datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(handler)
    if DEBUG:
        console_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(console_handler)
    log_level_int = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
    }[log_level]
    logger.log(log_level_int, message, *args, **kwargs)

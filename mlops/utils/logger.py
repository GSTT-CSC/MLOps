import logging
import colorlog
import sys
import time
import os
from pathlib import Path
home = str(Path.home())

os.makedirs(os.path.join(home, 'MLOPS_LOGS'), exist_ok=True)
LOG_FILE: str = os.path.join(home, 'MLOPS_LOGS', f'{time.strftime("%Y%m%d-%H%M%S")}_MLOps_logger.log')


def configure_logger():
    """
    Defined MLOps logger
    logs are stored in the file defined by LOG_FILE
    :return:
    """

    # make log formatters
    stream_formatter = colorlog.ColoredFormatter('%(log_color)s%(asctime)-15s %(levelname).1s '
                                                 '[%(filename)s:%(funcName)s:%(lineno)d] %(message)s',
                                                 '%Y-%m-%d %H:%M:%S')

    file_formatter = logging.Formatter('%(asctime)-15s %(levelname).1s [%(filename)s:%(funcName)s:%(lineno)d]'
                                       ' %(message)s',
                                       '%Y-%m-%d %H:%M:%S')

    stream_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(LOG_FILE)

    # set formatters
    stream_handler.setFormatter(stream_formatter)
    file_handler.setFormatter(file_formatter)

    # add handlers
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    # set logging level
    file_handler.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.INFO)

    logger.setLevel(logging.DEBUG)


logger = logging.getLogger(__name__)
configure_logger()

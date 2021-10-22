import logging
import colorlog
import sys


def configure_logger():

    # make log formatters
    stream_formatter = colorlog.ColoredFormatter('%(log_color)s%(asctime)-15s %(levelname).1s '
                                                 '[%(filename)s:%(funcName)s:%(lineno)d] %(message)s',
                                                 '%Y-%m-%d %H:%M:%S')

    file_formatter = logging.Formatter('%(asctime)-15s %(levelname).1s [%(filename)s:%(funcName)s:%(lineno)d]'
                                       ' %(message)s',
                                       '%Y-%m-%d %H:%M:%S')

    log_file = 'MLOps_logger.log'
    stream_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(log_file)

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

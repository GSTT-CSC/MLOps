import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ReleaseDestination(ABC):

    def __init__(self):
        logger.info(f'Creating ReleaseDestination: {self.__class__.__name__}')

    @abstractmethod
    def push(self, item):
        """
        ite
        :return:
        """
        raise NotImplementedError(
            f'Error in {repr(self.__class__.__name__)}: the class requires a collect method')

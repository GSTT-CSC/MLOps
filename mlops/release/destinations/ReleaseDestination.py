import logging
import json
import os
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ReleaseDestination(ABC):

    def __init__(self):
        logger.info(f'Creating ReleaseDestination: {self.__class__.__name__}')
        self.remote_artifacts = {}

    @abstractmethod
    def push(self, item):
        """
        Push artifacts to location - must be overwritten by subclass
        :return:
        """
        raise NotImplementedError(
            f'Error in {repr(self.__class__.__name__)}: the class requires a collect method')

    def write_destination_artifacts(self, filename='remote_artifacts.json'):
        """
        writes artifact paths to file
        :return:
        """
        logger.debug(f'Writing self.remote_artifacts to file')

        os.makedirs('.mlops', exist_ok=True)
        with open(f'.mlops/{filename}', 'w') as f:
            f.write(json.dumps(self.remote_artifacts))

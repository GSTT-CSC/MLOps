import logging
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


class ReleaseSource(ABC):

    def __init__(self, **kwargs):
        logger.info(f'Creating ReleaseSource: {self.__class__.__name__}')

        for k, v in kwargs.items():
            setattr(self, k, v)
        self.release_artifacts = {}
        self.remote_destination = None

    @abstractmethod
    def collect(self) -> Any:
        """
        Override this method to fetch release artifacts from release source
        """
        raise NotImplementedError(f'Error in {repr(self.__class__.__name__)}: the class requires a collect method')

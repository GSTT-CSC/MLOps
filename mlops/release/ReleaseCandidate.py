from abc import ABC, abstractmethod
from typing import Any


class ReleaseCandidate(ABC):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.release_artifacts = {}

    @abstractmethod
    def collect(self) -> Any:
        """
        Override this method to fetch release artifacts from release source
        """
        raise NotImplementedError(f'Error in {repr(self.__class__.__name__)}: You must define a collect method on this task')

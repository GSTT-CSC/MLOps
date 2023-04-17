from abc import ABC, abstractmethod
from typing import Any
from mlops.release.sources.MLFlowCandidate import MLFLowCandidate


class Release:

    def __init__(self, release_target, source='mlflow'):
        self.release_target = release_target
        self.source = source
        self.release_candidate = None

    def release(self):
        if self.source == 'mlflow':
            self.release_candidate = MLFLowProject(self.release_target)
        else:
            raise Exception(f'Unknown release source: "{self.release}"')

        self.release_candidate.run()

    def push_release(self):
        pass


class ReleaseCandidate(ABC):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.release_artifacts = {}

    def __str__(self):
        return 'ReleaseCandidate({})'.format(self._name)

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def run(self) -> Any:
        """
        Override this method to fetch release artifacts from release source
        """
        raise NotImplementedError(f'Error in {repr(self.__name__)}: You must define a run method on this task')

import logging

from mlops.release.destinations import LocalDestination, SharepointDestination, ReleaseDestination
from mlops.release.sources import MLFlowSource

logger = logging.getLogger(__name__)


class Release:

    def __init__(self, release_target, release_source, release_destination):
        self.source = None
        self.destination = None

        self.release_target = release_target
        self.release_source = release_source
        self.release_destination = release_destination

    def release(self):

        # Create release source
        if self.release_source == 'mlflow':
            self.source = MLFlowSource(self.release_target)
        else:
            raise Exception(f'Unknown release source: "{self.release}"')
        logger.info(f'Created release source: {self.source.__class__.__name__}')

        # Create release destination
        if self.release_destination == 'sharepoint':
            self.destination = SharepointDestination()
        elif self.release_destination == 'local':
            self.destination = LocalDestination()
        else:
            raise Exception(f'Unknown release destination: "{self.destination}"')
        logger.info(f'Created release destination: {self.destination.__class__.__name__}')

        # Collect release artifacts and push to storage
        self.source.collect()
        self.push_artifacts(self.source.release_artifacts, destination=self.destination)

    def push_artifacts(self, release_artifacts: dict = None, destination: ReleaseDestination = None):
        """
        Pushes artifacts to destination
        :return:
        """
        for k, v in release_artifacts.items():
            # push k as v
            pass

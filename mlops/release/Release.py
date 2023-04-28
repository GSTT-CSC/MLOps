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

        # Create release destination
        if self.release_destination == 'local':
            self.destination = LocalDestination()
        elif self.release_destination == 'sharepoint':
            self.destination = SharepointDestination()
        else:
            raise Exception(f'Unknown release destination: "{self.destination}"')

        # Collect release artifacts and push to storage
        self.source.collect()
        destination_paths = self.destination.push(self.source.release_artifacts)
        self.build_release()

    def build_release(self):
        pass

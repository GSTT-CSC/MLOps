import logging
import subprocess

from mlops.release.destinations import LocalDestination, SharepointDestination, ZenodoDestination
from mlops.release.sources import LocalSource, MLFlowSource

logger = logging.getLogger(__name__)


class Release:

    def __init__(self, config):
        self.source = None
        self.destination = None

        self.release_source = config['source']
        self.release_destination = config['destination']
        self.release_builder = config['builder']

    def release(self):

        # Create release source
        if 'mlflow' in self.release_source.keys():
            self.source = MLFlowSource(self.release_source['mlflow'])
        elif 'local' in self.release_source.keys():
            self.source = LocalSource(self.release_source['local'])
        else:
            raise Exception(f'Unrecognised release source: "{self.release_source}"')

        # Create release destination
        if 'local' in self.release_destination.keys():
            self.destination = LocalDestination(self.release_destination['local'])
        elif 'sharepoint' in self.release_destination.keys():
            self.destination = SharepointDestination(self.release_destination['sharepoint'])
        elif 'zenodo' in self.release_destination.keys():
            self.destination = ZenodoDestination(self.release_destination['zenodo'])
        else:
            raise Exception(f'Unrecognised release destination: "{self.release_destination}"')

        # Collect release artifacts and push to storage
        self.source.collect()
        self.destination.push(self.source.release_artifacts)
        self.build_release()

    def build_release(self):
        for cmd in self.release_builder:
            logger.debug(f'CMD: {cmd}')
            result = subprocess.run(cmd, shell=True, check=True)
        return result
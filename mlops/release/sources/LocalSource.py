import logging

from mlops.release.sources import ReleaseSource

logger = logging.getLogger(__name__)


class LocalSource(ReleaseSource):

    def __init__(self, config):
        super(LocalSource, self).__init__()
        self.config = config

    def collect(self):
        """
        The run method needs to populate the `self.artifacts` property, a dict that contains the build artifacts.
        :return:
        """
        self.release_artifacts = {}
        for item in self.config['artifacts']:
            # todo requires error handling
            self.release_artifacts[str(item)] = item

        logger.info(f'Collected artifacts: {self.release_artifacts}')

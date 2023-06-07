import logging

import mlflow

from mlops.release.sources import ReleaseSource

logger = logging.getLogger(__name__)


class MLFlowSource(ReleaseSource):

    def __init__(self, config):
        super(MLFlowSource, self).__init__()
        self.config = config

    def collect(self):
        """
        The run method needs to populate the `self.artifacts` property, a dict that contains the build artifacts.
        :return:
        """
        self.release_artifacts = {}
        for item in self.config['artifacts']:
            # todo requires error handling
            self.release_artifacts[str(item)] = mlflow.artifacts.download_artifacts(artifact_uri=item,
                                                                                    tracking_uri='http://0.0.0.0:85')

        logger.info(f'Collected artifacts: {self.release_artifacts}')

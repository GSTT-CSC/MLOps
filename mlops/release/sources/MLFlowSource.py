import os

from mlops.release.sources import ReleaseSource
import logging
import mlflow

logger = logging.getLogger(__name__)


class MLFlowSource(ReleaseSource):

    def __init__(self, run_id):
        super(MLFlowSource, self).__init__()
        self.mlflow_id = run_id

    def collect(self):
        """
        The run method needs to populate the `self.artifacts` property, a dict that contains the build artifacts.
        :return:
        """
        # todo requires error handling
        self.release_artifacts = {
                'model': mlflow.artifacts.download_artifacts(artifact_uri=self.mlflow_id,
                                                             tracking_uri='http://0.0.0.0:85')
            }
        logger.info(f'Collected artifacts: {self.release_artifacts}')

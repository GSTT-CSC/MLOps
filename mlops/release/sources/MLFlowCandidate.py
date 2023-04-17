import os

from mlops.release import ReleaseCandidate
import logging
import mlflow

logger = logging.getLogger(__name__)


class MLFLowCandidate(ReleaseCandidate):

    def __init__(self, run_id):
        super(MLFLowCandidate, self).__init__()
        self.mlflow_id = run_id

    def collect(self):
        """
        The run method needs to populate the `self.artifacts` property, a dict that contains the build artifacts.
        :return:
        """
        # os.environ['MLFLOW_TRACKING_URI'] = 'http://0.0.0.0:85'
        self.release_artifacts = {
                'model': mlflow.artifacts.download_artifacts(artifact_uri=self.mlflow_id,
                                                             tracking_uri='http://0.0.0.0:85')
            }

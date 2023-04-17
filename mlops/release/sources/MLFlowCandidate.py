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
        logger.info(f"Collecting {self.__class__.__name__} build artifacts")

        pass

    def get_artifacts(self):
        pass

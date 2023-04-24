from mlops.release.sources import MLFlowSource
import logging

logger = logging.getLogger(__name__)


class Release:

    def __init__(self, release_target, release_source):
        self.release_target = release_target
        self.source = release_source
        self.release_candidate = None

    def release(self):

        # Create candidate from release source
        if self.source == 'mlflow':
            self.release_candidate = MLFlowSource(self.release_target)
        else:
            raise Exception(f'Unknown release source: "{self.release}"')

        logger.info(f'Created release candidate: {self.release_candidate.__class__.__name__}')

        # Collect release artifacts and push to storage
        self.release_candidate.collect()
        self.push_artifacts(self.release_candidate.release_artifacts)

    def push_artifacts(self, release_artifacts: dict = None):
        """
        Pushes artifacts to location defined by remote_destination attr
        :return:
        """
        for k, v in release_artifacts.items():
            # push k as v
            pass

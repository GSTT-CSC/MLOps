from mlops.release.sources import MLFLowCandidate
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
            self.release_candidate = MLFLowCandidate(self.release_target)
        else:
            raise Exception(f'Unknown release source: "{self.release}"')

        logger.info(f'Created release candidate: {self.release_candidate.__class__.__name__}')

        # Collect release artifacts and push to remote storage
        self.release_candidate.collect()
        logger.info(f'Created release candidate: {self.release_candidate.__class__.__name__}')
        self.release_candidate.push_artifacts()


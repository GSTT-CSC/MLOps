import logging
from abc import ABC

from .ReleaseDestination import ReleaseDestination

logger = logging.getLogger(__name__)


class LocalDestination(ReleaseDestination, ABC):
    """
    Class to handle model artifacts stored on local file system
    """

    def __init__(self, config):
        super(LocalDestination, self).__init__()

    def push(self, release_artifacts: dict = None) -> dict:
        """
        Local destination already has files on disk after collect method called by ReleaseSource, push method has no effect but adds destination paths
        :param release_artifacts:
        :return:
        """
        logger.info(f'Pushing {len(release_artifacts)} items')
        destination_paths = {}
        return destination_paths

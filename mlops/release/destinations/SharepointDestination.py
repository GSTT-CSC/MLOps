from abc import ABC

from .ReleaseDestination import ReleaseDestination


class SharepointDestination(ReleaseDestination, ABC):
    """
    Class to handle uploading artifacts to sharepoint
    """

    def __init__(self, config):
        super(SharepointDestination, self).__init__()
        self.remote_path = 'mlops-artifacts'

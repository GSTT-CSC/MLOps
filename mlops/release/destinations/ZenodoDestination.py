import logging
import os
import shutil
from abc import ABC

import requests
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

from .ReleaseDestination import ReleaseDestination

logger = logging.getLogger(__name__)


class ZenodoDestination(ReleaseDestination, ABC):
    """
    Class to handle model artifacts stored on local file system
    """

    def __init__(self, config):
        super(ZenodoDestination, self).__init__()
        self.config = config
        self.params = {"access_token": self.config['access_token']}
        self.bucket_url = self.get_url()
        self.remote_artifacts = {}

    def get_url(self):
        # Get bucket URL
        res = requests.post(
            "https://zenodo.org/api/deposit/depositions",
            params=self.params,
            json={},
            headers={"Content-Type": "application/json"}
        )
        return res.json()["links"]["bucket"]

    def push(self, release_artifacts: dict = None) -> dict:
        """
        pushes artifacts to zenodo
        :param release_artifacts:
        :return:
        """
        logger.info(f'Pushing {len(release_artifacts)} items')
        for artifact_name, artifact_path in release_artifacts.items():
            logger.info(f'Uploading {artifact_name} ...')
            file_size = os.stat(artifact_path).st_size
            if os.path.isdir(artifact_path):
                logger.debug(f'Compressing directory {artifact_name}')
                artifact_path = shutil.make_archive(artifact_path, 'zip', artifact_path)

            with open(artifact_path, "rb") as f:
                with tqdm(total=file_size, unit="B", unit_scale=True, unit_divisor=1024) as t:
                    wrapped_file = CallbackIOWrapper(t.update, f, "read")
                    r = requests.put(
                        self.bucket_url + "/" + os.path.basename(artifact_path),
                        data=wrapped_file,
                        params=self.params,
                    )

            self.remote_artifacts[artifact_name] = r.json()['links']['self']

    def pull(self):
        """
        pulls artifacts from destination
        :return:
        """
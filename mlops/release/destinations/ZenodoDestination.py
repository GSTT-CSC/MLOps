from abc import ABC
import logging
import os
import shutil
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
        self.get_url()

    def get_url(self):
        # Get bucket URL
        res = requests.post(
            "https://zenodo.org/api/deposit/depositions",
            params=self.params,
            json={},
            headers={"Content-Type": "application/json"}
        )
        self.bucket_url = res.json()["links"]["bucket"]

    def push(self, release_artifacts: dict = None) -> dict:
        """
        Local destination already has files on disk after collect method called by ReleaseSource, push method has no effect but adds destination paths
        :param release_artifacts:
        :return:
        """
        logger.info(f'Pushing {len(release_artifacts)} items')
        for art_name, art_path in release_artifacts.items():
            logger.info(f'Uploading {art_name} ...')
            file_size = os.stat(art_path).st_size
            if os.path.isdir(art_path):
                logger.debug(f'compressing directory {art_name}')
                art_path = shutil.make_archive(art_path, 'zip', art_path)

            with open(art_path, "rb") as f:
                with tqdm(total=file_size, unit="B", unit_scale=True, unit_divisor=1024) as t:
                    wrapped_file = CallbackIOWrapper(t.update, f, "read")
                    r = requests.put(
                        self.bucket_url + "/" + os.path.basename(art_path),
                        data=wrapped_file,
                        params=self.params,
                    )

        return  r.json()


import logging
from mlops.release.Release import Release
from mlops.cli import parse_config

logger = logging.getLogger(__name__)

release_config = 'tests/mlops/release/data/release_config.yml'


class TestRelease:

    def setup(self):
        # currently only testing localhost code
        conf = parse_config(release_config)
        self.release = Release(conf)

    def test_release(self):
        pass
        # self.release.release()

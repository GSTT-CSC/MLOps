import logging
from mlops.release.Release import Release

logger = logging.getLogger(__name__)

# release_target = 'models:/hipposeg/Production'
# release_source = 'mlflow'
# release_destination = 'local'
# release_configuration = ''
release_config = 'tests/mlops/release/data/release_config.yml'


class TestRelease:

    def setup(self):
        # currently only testing localhost code
        self.release = Release(release_config)

    def test_release(self):
        pass
        # self.release.release()

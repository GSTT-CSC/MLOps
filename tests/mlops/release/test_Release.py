import logging
from mlops.release import Release

logger = logging.getLogger(__name__)

release_target = 'models:/hipposeg/Production'
release_source = 'mlflow'
release_destination = 'local'
release_configuration = ''


class TestRelease:

    def setup(self):
        # currently only testing localhost code
        self.release = Release(release_target, release_source, release_destination)

    def test_release(self):
        self.release.release()

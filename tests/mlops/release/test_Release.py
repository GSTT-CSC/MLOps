import logging
from mlops.release import Release

logger = logging.getLogger(__name__)

release_target = ''
release_source = ''
release_destination = ''


class TestRelease:

    def setup(self):
        # currently only testing localhost code
        self.release = Release(release_target, release_source, release_destination)

    def test_release(self):
        self.release.release()
        pass

    def test_push_artifacts(self):
        pass

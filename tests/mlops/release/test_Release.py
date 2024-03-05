import logging
from mlops.release.Release import Release
from mlops.cli import parse_config

logger = logging.getLogger(__name__)

release_config = 'tests/mlops/release/data/release_config_local.yml'


class TestRelease:

    def setup_method(self):
        # currently only testing localhost code
        conf = parse_config(release_config)
        self.release = Release(conf)

    def test_release(self):
        self.release.release()
        assert len(self.release.source.release_artifacts) == 1
        assert self.release.source.release_artifacts['tests/data/requirements.txt'] == 'tests/data/requirements.txt'

    def test_build_release(self):
        result = self.release.build_release()
        assert result.returncode == 0

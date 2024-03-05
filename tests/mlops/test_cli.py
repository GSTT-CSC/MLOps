from click.testing import CliRunner
from mlops.cli import run, release, parse_config


class TestCLI:

    def setup_method(self):
        self.test_config = 'tests/mlops/release/data/release_config_local.yml'

    def test_run(self):
        runner = CliRunner()
        result = runner.invoke(run, ['-h'])
        assert result.exit_code == 0

    def test_release(self):
        runner = CliRunner()
        result = runner.invoke(release, ['-h'])
        assert result.exit_code == 0

    def test_parse_config(self):
        conf = parse_config(self.test_config)
        assert len(conf) == 3
        assert conf['source']['local'] == {'artifacts': ['tests/data/requirements.txt']}

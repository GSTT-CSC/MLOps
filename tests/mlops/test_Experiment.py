from mlops.Experiment import Experiment
import pytest


class TestExperiment:

    def setup(self):
        self.experiment = Experiment('tests/config/test_config.cfg')

    @pytest.mark.skip(reason="placeholder for test")
    def test_config_setup(self):
        pass

    @pytest.mark.skip(reason="placeholder for test")
    def test_read_config(self):
        pass

    @pytest.mark.skip(reason="placeholder for test")
    def test_init_experiment(self):
        pass

    @pytest.mark.skip(reason="placeholder for test")
    def test_print_experiment_info(self):
        pass

    @pytest.mark.skip(reason="placeholder for test")
    def test_configure_minio(self):
        pass

    @pytest.mark.skip(reason="placeholder for test")
    def test_build_experiment_image(self):
        pass

    @pytest.mark.skip(reason="placeholder for test")
    def test_build_project_file(self):
        pass

    @pytest.mark.skip(reason="placeholder for test")
    def test_run(self):
        pass

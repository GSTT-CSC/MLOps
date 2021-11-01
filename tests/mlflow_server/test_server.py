from mlops.Experiment import Experiment


class TestExperiment:

    def setup(self):
        # currently only testing localhost code
        use_localhost = True
        self.experiment = Experiment('tests/data/test_config.cfg', use_localhost=use_localhost)

    def test_log_artifact(self):
        """Test to log artifact and then check it is available on MINIO"""
        pass

    def test_log_artifact(self):
        """Test to log artifact and then check it is available on MINIO"""
        pass

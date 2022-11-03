from mlops.Experiment import Experiment


class TestExperiment:

    def setup(self):
        # currently only testing localhost code
        self.experiment = Experiment('test_entry.py', config_path='tests/data/test_config.cfg', project_path='tests/data')


    def test_log_artifact(self):
        """Test to log artifact and then check it is available on MINIO"""
        pass

    def test_log_artifact(self):
        """Test to log artifact and then check it is available on MINIO"""
        pass

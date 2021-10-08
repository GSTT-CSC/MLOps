from mlops.Experiment import Experiment
import pytest
import configparser
from minio import Minio
import os

class TestExperiment:

    def setup(self):
        # currently only testing localhost code
        use_localhost = True
        self.experiment = Experiment('tests/data/test_config.cfg', use_localhost=use_localhost)

    @pytest.mark.skip(reason="placeholder for test")
    def test_config_setup(self):
        pass

    def test_env_setup(self):
        self.experiment.env_setup()
        assert os.getenv('MLFLOW_TRACKING_URI') == self.experiment.config['server']['LOCAL_REMOTE_SERVER_URI']
        assert os.getenv('MLFLOW_S3_ENDPOINT_URL') == self.experiment.config['server']['LOCAL_MLFLOW_S3_ENDPOINT_URL']
        assert os.getenv('AWS_ACCESS_KEY_ID') == self.experiment.config['user']['AWS_ACCESS_KEY_ID']
        assert os.getenv('AWS_SECRET_ACCESS_KEY') == self.experiment.config['user']['AWS_SECRET_ACCESS_KEY']

    def test_read_config(self):
        # Create config file and assert identical
        self.test_config = configparser.ConfigParser()
        self.test_config.read(self.experiment.config_path)
        assert self.experiment.config == self.test_config

    @pytest.mark.skip(reason="placeholder for test")
    def test_init_experiment(self):
        pass

    @pytest.mark.skip(reason="placeholder for test")
    def test_print_experiment_info(self, capsys):
        # Check correct information is printed to console
        self.experiment.print_experiment_info()  # Call function.
        captured = capsys.readouterr()
        assert captured.out == 'Building project file\nLogging to existing experiment: test_project *** ID: 1\nName: test_project\nExperiment_id: 1\nArtifact Location: s3://mlflow\nTags: {}\nLifecycle_stage: active\nName: test_project\nExperiment_id: 5\nArtifact Location: s3://mlflow\nTags: {}\nLifecycle_stage: active\n'

    def test_configure_minio(self):
        # check mlflow bucket is craeted
        self.experiment.configure_minio()
        client = Minio(self.experiment.uri_formatted, self.experiment.minio_cred['user'], self.experiment.minio_cred['password'], secure=False)
        assert 'mlflow' in (bucket.name for bucket in client.list_buckets())

    @pytest.mark.skip(reason="placeholder for test")
    def test_build_experiment_image(self):
        self.experiment.build_experiment_image()

    @pytest.mark.skip(reason="placeholder for test")
    def test_build_project_file(self):
        pass

    @pytest.mark.skip(reason="placeholder for test")
    def test_run(self):
        pass

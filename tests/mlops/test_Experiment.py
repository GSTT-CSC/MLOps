from mlops.Experiment import Experiment
import configparser
from minio import Minio
import os
import docker
import pytest


class TestExperiment:

    def setup(self):
        # currently only testing localhost code
        self.experiment = Experiment('tests/data/test_config.cfg', project_path='tests/data', use_localhost=True)

    def test_check_dirty(self):
        """
        Test that the local and remote experiments are the same
        """
        # Need to set project_path at level of git directory for this test.
        self.experiment = Experiment('tests/data/test_config.cfg', project_path='.', use_localhost=True)
        assert not self.experiment.check_dirty()

    def test_check_environment_variables(self):
        test_var = os.environ['AWS_ACCESS_KEY_ID']
        del os.environ['AWS_ACCESS_KEY_ID']
        with pytest.raises(Exception) as e:
            self.experiment.check_environment_variables()
        # reset env var
        os.environ['AWS_ACCESS_KEY_ID'] = test_var

    def test_config_setup(self):
        self.experiment.config_setup()
        assert self.experiment.experiment_name == 'test_project'
        assert self.experiment.artifact_path == 's3://mlflow'

    def test_env_setup(self):
        self.experiment.env_setup()
        assert os.getenv('MLFLOW_TRACKING_URI') == self.experiment.config['server']['LOCAL_REMOTE_SERVER_URI']
        assert os.getenv('MLFLOW_S3_ENDPOINT_URL') == self.experiment.config['server']['LOCAL_MLFLOW_S3_ENDPOINT_URL']

    def test_read_config(self):
        # Create config file and assert identical
        self.test_config = configparser.ConfigParser()
        self.test_config.read(self.experiment.config_path)
        assert self.experiment.config == self.test_config

    def test_init_experiment(self):
        self.experiment.init_experiment()
        assert self.experiment.experiment_id == '1'
        self.experiment.experiment_name = 'test_project_init_experiment'
        self.experiment.init_experiment()
        assert self.experiment.experiment_id == '2'

    def test_print_experiment_info(self, caplog):
        # Check correct information is printed to console
        self.experiment.print_experiment_info()  # Call function.
        assert 'Name: test_project' in caplog.text
        assert 'Artifact Location: s3://mlflow' in caplog.text

    def test_configure_minio(self):
        # check mlflow bucket is created
        self.experiment.configure_minio()
        client = Minio(self.experiment.uri_formatted,
                       self.experiment.minio_cred['user'],
                       self.experiment.minio_cred['password'],
                       secure=False)
        assert 'mlflow' in (bucket.name for bucket in client.list_buckets())

    def test_build_project_file(self):
        if os.path.exists('MLproject'):
            os.remove('MLproject')
        self.experiment.build_project_file()
        assert os.path.exists(os.path.join(self.experiment.project_path, 'MLproject'))

    def test_build_experiment_image(self):
        client = docker.from_env()
        images_1 = [img['RepoTags'][0] for img in client.api.images()]
        # assert self.experiment.experiment_name + ':latest' not in images_1
        self.experiment.build_experiment_image()
        images_2 = [img['RepoTags'][0] for img in client.api.images()]
        assert self.experiment.experiment_name + ':latest' in images_2

    def test_run(self, capsys):
        """
        this test will fail locally,  setup git in test data dir is done in github actions
        :param capsys:
        :return:
        """
        os.getcwd()
        self.experiment.build_project_file()
        self.experiment.run()
        captured = capsys.readouterr()
        assert 'succeeded' in captured.err

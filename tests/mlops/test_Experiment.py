from mlops.Experiment import Experiment
import configparser
from minio import Minio
import os
import docker


class TestExperiment:

    def setup(self):
        # currently only testing localhost code
        use_localhost = True
        os.environ['MINIO_ROOT_USER'] = 'minioadmin'
        os.environ['MINIO_ROOT_PASSWORD'] = 'minioadmin'
        self.experiment = Experiment('tests/data/test_config.cfg', use_localhost=use_localhost)

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
        assert False  # intentionally fail test

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
        if os.path.exists('MLProject'):
            os.remove('MLProject')
        self.experiment.build_project_file()
        assert os.path.exists('MLProject')

    def test_run(self, capsys):
        os.getcwd()
        self.experiment.build_project_file(path='tests/data/')
        self.experiment.run(path='tests/data/')
        captured = capsys.readouterr()
        assert 'succeeded' in captured.err

    def test_build_experiment_image(self):
        client = docker.from_env()
        images_1 = [img['RepoTags'][0] for img in client.api.images()]
        assert self.experiment.experiment_name + ':latest' not in images_1
        self.experiment.build_experiment_image(path='tests/data/')
        images_2 = [img['RepoTags'][0] for img in client.api.images()]
        assert self.experiment.experiment_name + ':latest' in images_2

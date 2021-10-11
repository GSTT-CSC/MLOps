import mlflow
import os
import configparser
import docker
from docker.errors import BuildError
from minio import Minio
from mlops.ProjectFile import ProjectFile


class Experiment:

    def __init__(self, config_path='config.cfg', use_localhost=False, verbose=True):

        self.config = None
        self.artifact_path = None
        self.experiment_name = None
        self.experiment_id = None
        self.config_path = config_path
        self.use_localhost = use_localhost
        self.verbose = verbose

        self.config_setup()
        self.env_setup()
        self.build_project_file()
        self.init_experiment()

        if self.verbose:
            self.print_experiment_info()

    def config_setup(self):

        self.read_config()
        self.artifact_path = self.config['server']['ARTIFACT_PATH']
        self.experiment_name = self.config['project']['NAME'].lower()

    def env_setup(self):
        if self.use_localhost:
            os.environ['MLFLOW_TRACKING_URI'] = self.config['server']['LOCAL_REMOTE_SERVER_URI']
            os.environ['MLFLOW_S3_ENDPOINT_URL'] = self.config['server']['LOCAL_MLFLOW_S3_ENDPOINT_URL']
        else:
            os.environ['MLFLOW_TRACKING_URI'] = self.config['server']['REMOTE_SERVER_URI']
            os.environ['MLFLOW_S3_ENDPOINT_URL'] = self.config['server']['MLFLOW_S3_ENDPOINT_URL']

    def read_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)

    def init_experiment(self):
        experiment = mlflow.get_experiment_by_name(self.experiment_name)
        self.configure_minio()

        if experiment is None:
            exp_id = mlflow.create_experiment(self.experiment_name, artifact_location=self.artifact_path)
            print('Creating experiment: name: {0} *** ID: {1}'.format(self.experiment_name, exp_id))
        else:
            exp_id = experiment.experiment_id
            print('Logging to existing experiment: {0} *** ID: {1}'.format(self.experiment_name, exp_id))

        self.experiment_id = exp_id

    def print_experiment_info(self):
        experiment = mlflow.get_experiment(self.experiment_id)
        print("Name: {}".format(experiment.name))
        print("Experiment_id: {}".format(experiment.experiment_id))
        print("Artifact Location: {}".format(experiment.artifact_location))
        print("Tags: {}".format(experiment.tags))
        print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))

    def configure_minio(self):
        if self.use_localhost:
            self.uri_formatted = self.config['server']['LOCAL_MLFLOW_S3_ENDPOINT_URL'].replace("http://", "")
        else:
            self.uri_formatted = self.config['server']['MLFLOW_S3_ENDPOINT_URL'].replace("http://", "")

        self.minio_cred = {'user': os.getenv('MINIO_ROOT_USER'),
                           'password': os.getenv('MINIO_ROOT_PASSWORD')}

        client = Minio(self.uri_formatted, self.minio_cred['user'], self.minio_cred['password'], secure=False)
        # if mlflow bucket does not exist, create it
        if 'mlflow' not in (bucket.name for bucket in client.list_buckets()):
            print('Creating S3 bucket ''mlflow''')
            client.make_bucket("mlflow")

    def build_experiment_image(self, path: str = '.'):
        print('Building experiment image ...')

        # Collect proxy settings
        build_args = {}
        if os.getenv('HTTP_PROXY') is not None or os.getenv('HTTPS_PROXY') is not None:
            build_args = {'HTTP_PROXY': os.getenv('HTTP_PROXY'),
                          'HTTPS_PROXY': os.getenv('HTTPS_PROXY')}

        client = docker.from_env()
        client.images.build(path=path,
                            tag=self.experiment_name,
                            buildargs=build_args,
                            rm=True)

    def build_project_file(self):
        print('Building project file')
        projectfile = ProjectFile(self.config, use_localhost=self.use_localhost)
        projectfile.generate_yaml()

    def run(self, remote: str = None, **kwargs):
        print('Starting experiment ...')

        docker_args_default = {'network': "host",
                               'ipc': 'host',
                               }

        if not self.use_localhost:
            gpu_params = {'gpus': 'all',
                          'runtime': 'nvidia'}
            print('Adding docker args: {0}'.format(gpu_params))
            docker_args_default.update(gpu_params)

        # update docker_args_default with values passed by project
        if 'docker_args' in kwargs:
            docker_args_default.update(kwargs['docker_args'])
            kwargs['docker_args'] = docker_args_default

        # check image exists and build if not
        print('checking for existing image')
        client = docker.from_env()
        images = [img['RepoTags'][0] for img in client.api.images()]
        if self.experiment_name + ':latest' not in images:
            print('No existing image found')
            self.build_project_file()

        mlflow.run('.',
                   experiment_id=self.experiment_id,
                   use_conda=False,
                   **kwargs)

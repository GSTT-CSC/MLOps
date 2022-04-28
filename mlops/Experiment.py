import mlflow
import os
import sys
import configparser
import docker
from minio import Minio
from mlops.ProjectFile import ProjectFile
from mlops.utils.logger import logger
from git import Repo


class Experiment:

    def __init__(self, config_path='config.cfg', project_path='.', use_localhost=False, verbose=True):

        self.config = None
        self.artifact_path = None
        self.experiment_name = None
        self.experiment_id = None
        self.config_path = config_path
        self.use_localhost = use_localhost
        self.project_path = project_path
        self.verbose = verbose

        if 'pytest' not in sys.modules:
            self.check_dirty()

        self.check_environment_variables()
        self.config_setup()
        self.env_setup()
        self.build_project_file()
        self.init_experiment()

        if self.verbose:
            self.print_experiment_info()

    def check_dirty(self):
        logger.debug('Comparing to remote git repository')
        repo = Repo(self.project_path)
        head = repo.head.ref
        tracking = head.tracking_branch()
        local_commits_ahead_iter = head.commit.iter_items(repo, f'{tracking.path}..{head.path}')
        commits_ahead = sum(1 for _ in local_commits_ahead_iter)

        if repo.is_dirty():
            raise Exception('Repository is dirty. Please commit your changes before running the experiment')
        if commits_ahead > 0:
            raise Exception('Local repository ahead of remote. Please push changes before running the experiment')

        if not repo.is_dirty() and commits_ahead == 0:
            return False
        else:
            raise Exception('Please synchronise local and remote code versions before running the experiment')

    @staticmethod
    def check_environment_variables():
        required_env_variables = ['AWS_ACCESS_KEY_ID',
                                  'AWS_SECRET_ACCESS_KEY']

        for var in required_env_variables:
            if os.getenv(var) is None:
                raise Exception('{0} is a required environment variable: set with "export {0}=<value>"'.format(var))

    def config_setup(self):
        logger.info('reading config file: {0}'.format(self.config_path))
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
        # logger.info('Creating experiment: name: {0} *** ID: {1}'.format(self.experiment_name, exp_id))
        experiment = mlflow.get_experiment_by_name(self.experiment_name)

        if experiment is None:
            exp_id = mlflow.create_experiment(self.experiment_name, artifact_location=self.artifact_path)
            logger.info('Creating experiment: name: {0} *** ID: {1}'.format(self.experiment_name, exp_id))
        else:
            exp_id = experiment.experiment_id
            logger.info('Logging to existing experiment: {0} *** ID: {1}'.format(self.experiment_name, exp_id))

        logger.info('Setting tracking URI to: {0} '.format(os.environ['MLFLOW_TRACKING_URI']))
        mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])
        logger.info('Setting experiment to: {0} '.format(self.experiment_name))
        mlflow.set_experiment(self.experiment_name)
        self.configure_minio()
        self.experiment_id = exp_id

    def print_experiment_info(self):
        experiment = mlflow.get_experiment(self.experiment_id)
        logger.info("Name: {}".format(experiment.name))
        logger.info("Experiment_id: {}".format(experiment.experiment_id))
        logger.info("Artifact Location: {}".format(experiment.artifact_location))
        logger.info("Tags: {}".format(experiment.tags))
        logger.info("Lifecycle_stage: {}".format(experiment.lifecycle_stage))

    def configure_minio(self):
        if self.use_localhost:
            self.uri_formatted = self.config['server']['LOCAL_MLFLOW_S3_ENDPOINT_URL'].replace("http://", "")
        else:
            self.uri_formatted = self.config['server']['MLFLOW_S3_ENDPOINT_URL'].replace("http://", "")

        self.minio_cred = {'user': os.getenv('AWS_ACCESS_KEY_ID'),
                           'password': os.getenv('AWS_SECRET_ACCESS_KEY')}

        # todo: replace this with either a machine level IAM role or ~/.aws/credentials profile
        os.environ['MINIO_ROOT_USER'] = os.getenv('AWS_ACCESS_KEY_ID')
        os.environ['MINIO_ROOT_PASSWORD'] = os.getenv('AWS_SECRET_ACCESS_KEY')

        client = Minio(self.uri_formatted, self.minio_cred['user'], self.minio_cred['password'], secure=False)
        # if mlflow bucket does not exist, create it
        if 'mlflow' not in (bucket.name for bucket in client.list_buckets()):
            logger.info('Creating S3 bucket ''mlflow''')
            client.make_bucket("mlflow")

    def build_experiment_image(self, path: str = '.'):
        logger.info('Building experiment image ...')

        # Collect proxy settings
        build_args = {}
        if os.getenv('http_proxy') is not None or os.getenv('https_proxy') is not None:
            build_args = {'http_proxy': os.getenv('http_proxy'),
                          'https_proxy': os.getenv('https_proxy')}

        client = docker.from_env()
        logger.info('Running docker build with: {0}'.format({'path': self.project_path,
                                                              'tag': self.experiment_name,
                                                              'buildargs': build_args,
                                                              'rm': 'True'}))

        client.images.build(path=self.project_path,
                            tag=self.experiment_name,
                            buildargs=build_args,
                            rm=True)
        logger.info('Built: ' + self.experiment_name + ':latest')

    def build_project_file(self, path: str = '.'):
        logger.info('Building project file')
        projectfile = ProjectFile(self.config, path=self.project_path, use_localhost=self.use_localhost)
        projectfile.generate_yaml()

    def run(self, path: str = '.', remote: str = None, **kwargs):
        logger.info('Starting experiment ...')

        docker_args_default = {'network': "host",
                               'ipc': 'host',
                               'rm': ''
                               }

        if not self.use_localhost:
            gpu_params = {'gpus': 'all',
                          'runtime': 'nvidia'}
            logger.info('Adding docker args: {0}'.format(gpu_params))
            docker_args_default.update(gpu_params)

        # update docker_args_default with values passed by project
        if 'docker_args' in kwargs:
            docker_args_default.update(kwargs['docker_args'])
            kwargs['docker_args'] = docker_args_default

        # check image exists and build if not
        logger.info('Checking for existing image')
        client = docker.from_env()
        images = [str(img['RepoTags']) for img in client.api.images()]
        if all([(self.experiment_name + ':latest') not in item for item in images]):
            logger.info('No existing image found')
            self.build_experiment_image(path=self.project_path)
        else:
            logger.info('Found existing project image')

        artifact_uri = mlflow.get_artifact_uri()
        print("Artifact uri: {}".format(artifact_uri))

        mlflow.run(self.project_path,
                   experiment_id=self.experiment_id,
                   use_conda=False,
                   **kwargs)

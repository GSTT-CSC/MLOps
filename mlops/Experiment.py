import configparser
import os
import sys
from ast import literal_eval
import boto3
import docker
import mlflow
import torch.cuda
from git import Repo
import subprocess
import docker
import mlflow
from git import Repo
from minio import Minio
# from torch.cuda import is_available

from mlops.ProjectFile import ProjectFile
from mlops.utils.logger import logger, LOG_FILE


class Experiment:

    def __init__(self, script, config_path, project_path: str = '.',
                 verbose: bool = True, ignore_git_check: bool = False,
                 artifact_path: str = 's3://mlflow'):
        """
        The Experiment class is the interface through which all projects should be run.
        :param script: path to script to run
        :param config_path: string path to configuration file
        :param project_path: string path to project directory
        :param verbose: verbosity
        """
        self.script = script
        self.config = None
        self.artifact_path = artifact_path
        self.experiment_name = None
        self.experiment_id = None
        self.config_path = config_path
        self.project_path = project_path
        self.verbose = verbose
        self.auth = None

        if 'pytest' in sys.modules:
            logger.warn('DEBUG ONLY - ignoring git checks due to test run detected')

        elif ignore_git_check is True:
            logger.warn(
                'DEBUG ONLY - ignoring git checks, manually disabled. Ensure this run is not for any experiments '
                'intended for production use')
        else:
            self.check_dirty()
        self.check_minio_credentials()
        self.config_setup()
        self.use_gpu = self.check_gpu()
        self.env_setup()
        self.build_project_file()
        self.init_experiment()

        if self.verbose:
            self.print_experiment_info()

    def check_gpu(self):
        try:
            request_gpu = self.config.getboolean('system', 'USE_GPU')
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            logger.debug(f'GPU resource not explicitly requested {e} defaulting to True')
            request_gpu = True

        logger.info(f'GPU requested: {request_gpu}, cuda_available {torch.cuda.is_available()}')
        if torch.cuda.is_available() and request_gpu:
            return True
        else:
            return False

    def check_minio_credentials(self):
        self.auth = boto3.session.Session().get_credentials()
        if self.auth is None:
            logger.debug(f'Found minio credentials in {self.auth.method}')
            raise Exception(
                f'minio credentials not found - either specify in ~/.aws/credentials or using environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)')

    def check_dirty(self) -> bool:
        """
        Checks whether the git repository at self.project_path has any uncommmited changes (is_dirty) or if it has any
        local commits that are ahead of the remote. If either of these conditions are true  an exception is raised.
        :return:
        """
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

    def config_setup(self):
        """
        Reads the configuration file and extracts necessary values
        :return:
        """
        logger.info('reading config file: {0}'.format(self.config_path))
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)

        self.experiment_name = self.config['project']['NAME'].lower()

    def env_setup(self):
        """
        Stores the variables required for running mlflow projects with docker in the environment
        :return:
        """
        os.environ['MLFLOW_TRACKING_URI'] = self.config['server']['MLFLOW_TRACKING_URI']
        os.environ['MLFLOW_S3_ENDPOINT_URL'] = self.config['server']['MLFLOW_S3_ENDPOINT_URL']

    def init_experiment(self):
        """
        Initialises experiment for tracking with mlflow.

        Fetches experiment info from configured mlflow server. If it doesn't exist then one is created.
        :return:
        """
        logger.info(f'Initialising Experiment {self.experiment_name}')

        # Get experiment from mlflow server
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

        # self.configure_minio()
        self.experiment_id = exp_id

    def print_experiment_info(self):
        """
        Prints basic experiment info to logger
        :return:
        """
        experiment = mlflow.get_experiment(self.experiment_id)
        logger.info("Name: {}".format(experiment.name))
        logger.info("Experiment_id: {}".format(experiment.experiment_id))
        logger.info("Artifact Location: {}".format(experiment.artifact_location))
        logger.info("Tags: {}".format(experiment.tags))
        logger.info("Lifecycle_stage: {}".format(experiment.lifecycle_stage))

    def configure_minio(self):
        """
        configures the minio artifact storage.

        The minio auth credentials are fetched from the environment and used to create a bucket named "mlflow" for
        logging mlflow artifacts. If a bucket called mlflow already exists then the existing bucket is used.

        :return:
        """
        logger.info('Configuring Minio')
        self.uri_formatted = self.config['server']['MLFLOW_S3_ENDPOINT_URL'].replace("http://", "")

        self.minio_cred = {'user': os.getenv('AWS_ACCESS_KEY_ID'),
                           'password': os.getenv('AWS_SECRET_ACCESS_KEY')}

        # todo: replace this with either a machine level IAM role or ~/.aws/credentials profile
        os.environ['MINIO_ROOT_USER'] = os.getenv('AWS_ACCESS_KEY_ID')
        os.environ['MINIO_ROOT_PASSWORD'] = os.getenv('AWS_SECRET_ACCESS_KEY')

        client = Minio(self.uri_formatted, self.minio_cred['user'], self.minio_cred['password'], secure=False)

        if 'mlflow' not in (bucket.name for bucket in client.list_buckets()):
            logger.info('Creating S3 bucket ''mlflow''')
            client.make_bucket("mlflow")

    def build_experiment_image_subprocess(self, dockerfile_path = 'Dockerfile', context_path: str = '.', no_cache: bool = False, build_args: dict = {}):
        """
        Builds the Dockerfile at location path if parameter is supplied, else uses self.project_path (default)

        Images are tagged using the project name defined in config. If proxy variables exist in the environment these
        are passed to the docker demon as build arguments.

        :param context_path: optional path to Dockerfile (if not in project_path root)
        :return:
        """

        # Build dockerfile into an MAP image
        docker_build_cmd = f'docker build -f "{dockerfile_path}" -t {self.experiment_name} "{context_path}"'
        # if sys.platform != "win32":
        #     docker_build_cmd += """ --build-arg UID=$(id -u) --build-arg GID=$(id -g)"""
        if no_cache:
            docker_build_cmd += " --no-cache"
        if build_args:
            for k, v in build_args.items():
                docker_build_cmd += f' --build-arg {k}={v}'

        logger.info("Docker image build command: %s", docker_build_cmd)

        proc = subprocess.Popen(docker_build_cmd, stdout=subprocess.PIPE, shell=True)

        logger.info("Docker image build command: %s", docker_build_cmd)

        while proc.poll() is None:
            if proc.stdout:
                logger.debug(proc.stdout.readline().decode("utf-8"))

        # proc.wait()
        return_code = proc.returncode

        if return_code == 0:
            logger.info(f"Successfully built {self.experiment_name}")

    def build_project_file(self, path: str = '.'):
        """
        Builds MLProject yaml file used by mlflow to define the project. See the mlops.ProjectFile class for more info.
        :param path:
        :return:
        """
        logger.info('Building project file')
        projectfile = ProjectFile(self.config, self.config_path, self.script, path=self.project_path)
        projectfile.generate_yaml()

    def run(self, **kwargs):
        """
        Runs the mlflow project that has been defined by the MLProject file output by self.build_project_file

        After running the project the logs are stored as an artifact on the mlflow server.
        :param kwargs:
        :return:
        """
        rebuild_docker = kwargs.get('rebuild_docker', False)
        shared_memory = kwargs.get('shared_memory', '8gb')

        logger.info(f'Starting experiment: {self.experiment_name}')

        docker_args_default = {'network': "host",
                               'ipc': 'private',
                               'rm': '',
                               'shm-size': shared_memory
                               }

        if self.auth.method == 'shared-credentials-file':
            logger.debug(f'Mounting shared env file for minio authentication to /root/.aws')
            docker_args_default['v'] = '~/.aws/credentials:/root/.aws/credentials:ro'

        # if not self.use_localhost:
        # if self.use_gpu and not is_available():
        # if self.use_gpu and not is_available():
        #     logger.warn('requested GPU resource but none available - using CPU')
        # elif self.use_gpu and is_available():
        elif self.use_gpu:
            gpu_params = {'gpus': 'all',
                          'runtime': 'nvidia'}
            logger.info('Adding docker args: {0}'.format(gpu_params))
            docker_args_default.update(gpu_params)

        # update docker_args_default with values passed by project
        if 'docker_args' in kwargs:
            docker_args_default.update(kwargs['docker_args'])
            docker_args_default = docker_args_default

        # check image exists and build if not
        logger.info('Checking for existing image')
        client = docker.from_env()
        images = [str(img['RepoTags']) for img in client.api.images()]
        if all([(self.experiment_name + ':latest') not in item for item in images]) or rebuild_docker:
            logger.info(f'No existing image found, rebuild flag {rebuild_docker}')
            self.build_experiment_image_subprocess(context_path=self.project_path)
        else:
            logger.info(f'Found existing project image: {self.experiment_name}:latest')

        logger.debug(f'Artifact URI: {mlflow.get_artifact_uri()}')
        logger.debug(f'Project URI: {self.project_path}')

        mlflow.run(uri=self.project_path,
                   experiment_id=self.experiment_id,
                   env_manager='local',
                   build_image=True,  # revisit this in the future, mlflow 2.0 changed this behaviour, can we be more efficient?
                   docker_args=docker_args_default
                   )

        mlflow.log_artifact(LOG_FILE)

import mlflow
import os
import configparser
from docker.errors import BuildError
from io import BytesIO
from docker import APIClient

config = configparser.ConfigParser()
config.read('config.cfg')

experiment_name = 'mlflow_tests'
artifact_path = 's3://mlflow'
remote_server_uri = 'http://localhost:80'

os.environ['MLFLOW_TRACKING_URI'] = remote_server_uri
os.environ['MLFLOW_S3_ENDPOINT_URL'] = config['server']['MLFLOW_S3_ENDPOINT_URL']
os.environ['AWS_ACCESS_KEY_ID'] = config['user']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY'] = config['user']['AWS_SECRET_ACCESS_KEY']


def init_experiment(name, artifact_location=artifact_path):

    experiment = mlflow.get_experiment_by_name(name)

    if experiment is None:
        experiment_id = mlflow.create_experiment(name, artifact_location=artifact_location)
        print('Creating experiment: name: {0} *** ID: {1}'.format(name, experiment_id))
    else:
        experiment_id = experiment.experiment_id
        print('Logging to experiment: {0} *** ID: {1}'.format(name, experiment_id))

    return experiment_id


def print_experiment_info(experiment_id):
    experiment = mlflow.get_experiment(experiment_id)
    print("Name: {}".format(experiment.name))
    print("Experiment_id: {}".format(experiment.experiment_id))
    print("Artifact Location: {}".format(experiment.artifact_location))
    print("Tags: {}".format(experiment.tags))
    print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))


def build_docker_image():
    """builds dockerfile in cwd"""
    # f = BytesIO(dockerfile.encode('utf-8'))
    cli = APIClient(base_url='tcp://127.0.0.1:2375')
    response = [line for line in cli.build(path=os.getcwd(), rm=True, tag='mlflow-docker-test')]
    print(response)

# Configure experiment and run project
experiment_id = init_experiment(experiment_name)
print_experiment_info(experiment_id)

try:
    mlflow.run('.', docker_args={'network': 'host', 'rm': ''}, use_conda=False, experiment_id=experiment_id)
except BuildError:
    print('Have you built your project dockerfile? e.g. docker build -t project-tag -f Dockerfile .')


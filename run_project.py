import mlflow
import os
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

# Get these from config file eventually
experiment_name='mlflow_tests_12'
artifact_path='s3://mlflow'
remote_server_uri='http://localhost:80'

os.environ['MLFLOW_TRACKING_URI'] = remote_server_uri
os.environ['MLFLOW_S3_ENDPOINT_URL'] = config['server']['MLFLOW_S3_ENDPOINT_URL']
os.environ['AWS_ACCESS_KEY_ID'] = config['user']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY'] = config['user']['AWS_SECRET_ACCESS_KEY']


def init_experiment(name, artifact_location=artifact_path):
    # Create an experiment name, which must be unique and case sensitive
    try:
        experiment_id = mlflow.create_experiment(name, artifact_location=artifact_location)
        print('Created experiment: {}'.format(name))
    except mlflow.exceptions.MlflowException:
        print("experiment already exists: logging to existing")

    experiment_id = mlflow.set_experiment(name)
    experiment = mlflow.get_experiment(experiment_id)
    print("Name: {}".format(experiment.name))
    print("Experiment_id: {}".format(experiment.experiment_id))
    print("Artifact Location: {}".format(experiment.artifact_location))
    print("Tags: {}".format(experiment.tags))
    print("Lifecycle_stage: {}".format(experiment.lifecycle_stage))


init_experiment(experiment_name)
# Run MLflow test_project and create a reproducible conda environment
mlflow.run('.', docker_args={'network': 'host', 'rm': ''}, use_conda=False)

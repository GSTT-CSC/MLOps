import mlflow
import os

experiment_name = 'test experiment'
artifact_path = 's3://mlflow/test'
mlflow.set_tracking_uri('http://localhost:85')

experiment = mlflow.get_experiment_by_name(experiment_name)
if experiment is None:
    exp_id = mlflow.create_experiment(experiment_name, artifact_location=artifact_path)
    print('Creating experiment: name: {0} *** ID: {1}'.format(experiment_name, exp_id))
else:
    exp_id = experiment.experiment_id
    print('Logging to existing experiment: {0} *** ID: {1}'.format(experiment_name, exp_id))

mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])
mlflow.set_experiment(experiment_name)


with mlflow.start_run() as run:
    mlflow.log_metric("test", 0)

    artifact_uri = mlflow.get_artifact_uri()
    print("Artifact uri: {}".format(artifact_uri))

    mlflow.log_artifact("/home/hnadmin/MLOps/mlflow_server/test_mlflow.py")

"""
This script can be used to test the mlflow server has been properly configured. After setting up the server using

docker-compose up -d --build

log onto the minio server or use the API to create a bucket called 'mlflow' and set the AWS credentials and s3 endpoint
 (e.g.):

export MLFLOW_S3_ENDPOINT_URL=http://0.0.0.0:8002
export AWS_ACCESS_KEY_ID=minioadmin
export AWS_SECRET_ACCESS_KEY=minioadmin

python test_mlflow.py

Running this script will log a simple experiment to the artifact storage and the tracking server. Check that these are
available by accessing the UI's for minio (:8002) and mlflow (:85)
"""

import mlflow
import os
import pathlib

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

mlflow.set_experiment(experiment_name)

with mlflow.start_run() as run:
    mlflow.log_metric("test", 0)

    artifact_uri = mlflow.get_artifact_uri()
    print("Artifact uri: {}".format(artifact_uri))

    mlflow.log_artifact(os.path.join(pathlib.Path(__file__).parent.absolute(), 'test_mlflow.py'))

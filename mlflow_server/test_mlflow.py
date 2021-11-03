import mlflow

mlflow.set_tracking_uri("http://localhost:85")
mlflow.create_experiment("test_experiment", artifact_location='s3://mlflow/test')

with mlflow.start_run() as run:
    mlflow.log_metric("test", 0)


with mlflow.start_run() as run:
    artifact_uri = mlflow.get_artifact_uri()
    print("Artifact uri: {}".format(artifact_uri))
    mlflow.log_artifact("/home/hnadmin/MLOps/mlflow_server/test_mlflow.py")

mlflow.end_run()
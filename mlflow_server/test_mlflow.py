import mlflow

mlflow.set_tracking_uri("http://localhost:85")
mlflow.set_experiment("test_experiment")

with mlflow.start_run() as run:
    mlflow.log_metric("test", 0)


with mlflow.start_run() as run:
    mlflow.log_artifact("/home/hnadmin/MLOps/mlflow_server/test_mlflow.py")

mlflow.end_run()
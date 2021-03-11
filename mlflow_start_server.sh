#!/bin/bash

mlflow server \
    --backend-store-uri postgresql://root:root@localhost/mlflow_test \
    --default-artifact-root .mlflow_artifact_store \
    --host 0.0.0.0

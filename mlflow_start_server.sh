#!/bin/bash

mlflow server -p 5000 \
--host 0.0.0.0 \
--backend-store-uri postgresql://root:root@localhost/mlflow_test \
--default-artifact-root .mlflow_artifact_store
# MLOps requirements and software options


## Introduction
This document aims to outline the requirements we have identified for MLOps and how we might address them.

## Current proposal
| Category      | Details | Software candidates     |
| :---        |:----   |:--- |
| Data Versioning       | Tools to track data versions                        | options   |
| Model registry        | Tools to build end-to-end model training pipelines  | options   |
| Model serving         | Tools for model serving                             | options   |
| Model monitoring      | Tools for model monitoring                          | options   |
| CI/CD Orchestration   | Tools for streamlining CI/CD workflow               | options   |


## Requirements
This section summaries the main requirements we have identified for each.

### 1. Data Versioning
##### Background
##### Identified requirements:
1. Ability to store and recall any particular version of data that has been used to train a model.
2. Ability to associate any particular tagged data version to a particular trained model.
###### DVC, Pachyderm, Azure

### 2. Model registry
##### Background
When the right candidate for production is found, it is pushed to a model registry — a centralized hub capturing all metadata for published models such as name, version, date etc. The registry acts as a communication layer between research and production environments, providing a deployed model with the information it needs in runtime.
##### Identified requirements:
1. Ability to associate any trained model with a particular code and data version
###### MLflow Model Registry, AI Hub, Azure

### 3. Model Serving
##### Background
When a model is ready to be deployed a model serving tool can be used to automate and facilitate the process. Given we don't expect models to require frequent or continuous updates this requirement is a lower priority.
##### Identified requirements:
1. Provides a simple method for moving a tested and approved model to deployment
###### Docker, Seldon Core, MLflow Models, Algorithmia, Kubeflow, Azure

### 4. Model monitoring
##### Background
An interface is required to evaluate model performance following changes to code and/or data.  Additionally, after release to deployment, the model performance may be affected by numerous factors, such as an initial mismatch between training data and live populations. Monitoring is required to continuously review model performance on a live implementation.  
##### Identified requirements:
1. Ability to track testing and live model performance and associate performance metric with code and data versions.
###### Clear ML, MLWatcher, DbLue, Qualdo, Azure

### 5. CI/CD integration
##### Background
CI/CD/CT will benefit from processing data and models on local hardware
##### Identified requirements:
1. Functionality to run data processing/training on local hardware
2. Automatic execution of training pipeline
2. Conventional CI/CD tools: issue tracking, git integration, automated tests/pipelines.
###### Gitlab, Github/Azure

### Sources
1. https://www.altexsoft.com/blog/mlops-methods-tools/

<!-- PROJECT HEADING -->
<br />
<p align="center">
<a href="https://github.com/github_username/repo_name">
    <img src="https://raw.githubusercontent.com/GSTT-CSC/gstt-csc.github.io/main/assets/transparent-CSC-logo-cropped.png" alt="Logo" width="50%">
  </a>
<h1 align="center">MLOps</h1>
<p align="center">
A continuous integration and deployment framework for healthcare AI projects
<br />
<a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
<br />
<br />
<a href="https://github.com/GSTT-CSC/MLOps">View repo</a>
·
<a href="https://github.com/GSTT-CSC/MLOps/issues">Report Bug</a>
·
<a href="https://github.com/GSTT-CSC/MLOps/issues">Request Feature</a>
</p>
<p align="center">
  <img src="https://github.com/GSTT-CSC/MLOps/actions/workflows/master-develop-test.yml/badge.svg?branch=main">
  <img src="https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/laurencejackson/ba102d5f3e592fcd50451c2eff8a803d/raw/19cbafdaad049423cf20c725944c52a3ed3764e7/mlops_pytest-coverage-comment.json">
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#open-source-components">Open source components</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li>
      <a href="#getting-started-on-local-hardware">Getting Started On Local Hardware</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#overview">Overview</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
   <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project aims to build an effective MLOps framework for the development of AI models in a healthcare setting. 

### Open source components

* [MLflow](https://mlflow.org/) Open source platform to manage the ML lifecycle
* [MONAI](https://monai.io/) PyTorch-based framework for deep learning in healthcare imaging
* [MINIO](https://min.io/) High performance object storage suite
* [NGINX](https://www.nginx.com/) Reverse proxy server

It's not essential to have a complete understanding of all of these, but a high-level understanding of [MLflow](https://mlflow.org/) in particular will be useful!

The MLOps framework has two major components a server and an Experiment class that abstracts away a lot of the 
boilerplate that would otherwise be required to interface with the server. A high level overview of the framework is illustrated below:


![](docs/assets/mlops_map.png)


In this case we have illustrated the MLOps server and Experiment runner as separate machines, but there is no reason 
these cannot be the same machine by pointing the environment variables to the localhost address.


<!-- CONTRIBUTING -->
## Contributing
1. Fork or clone the Project
2. Since all code changes are staged on the `develop` branch before releases you will need to checkout this branch first (`git checkout -b develop`)
3. Create your Feature Branch off of `develop` (`git checkout -b feature/AmazingFeature`)
4. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the remote (`git push origin feature/AmazingFeature`)
6. Open a Pull Request and specifiy that you want to merge your feature branch into the `develop` branch

### Testing
When contributing, you are _strongly_ encouraged to write tests for any functions or classes you add. Please uses pytest and add your tests to an appropriate location in the  `tests` directory, which also contains some examples to get you started.

<!-- GETTING STARTED  -->
## Getting Started On Local Hardware

The production version of this project is intended to run on a dedicated remote machine on an isolated network. However, it is simple to set up a local copy to get an understanding of the framework.


### Prerequisites

First follow the instructions to install [Docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/).
A basic understanding of how docker and docker-compose work is recommended, available below. 

* [Docker overview](https://docs.docker.com/get-started/overview/)
* [docker-compose overview](https://docs.docker.com/compose/)

Check docker and docker-compose are working by calling passing the help argument on the command line. If the help information is not returned, or an error is given revist the docker installation docs.
```sh
docker --help
docker-compose --help
```

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/GSTT-CSC/MLOps.git
   cd MLOps
   ```
   
2. The server should be configured by creating an environment file at ```/mlflow_server/.env```. The environment variable shown are given as an example, and should not be used for a production deployment.

Setting these variables is a requirement, the server will fail to start if they are undefined.

**Please do not use shown values. Consider Writing you own usernames and passwords.**

```
# Example env file - fill all required values before using
AWS_ACCESS_KEY_ID=minioUsername
AWS_SECRET_ACCESS_KEY=minioPassword
MLFLOW_S3_IGNORE_TLS=true
POSTGRES_USER=use
POSTGRES_PASSWORD=pass
POSTGRES_DB=db
```

3. Navigate to the cloned code repository and start the server. Any docker images that are not present on your local system will be pulled from dockerhub (which might take a while).
    ```sh
   cd mlflow_server
   docker-compose up -d --build
   ```

Upon a successful build the server should now be up and running locally, and should show similar output to the screenshot below. By default, the mlflow user interface can be accessed at ```http:/localhost:85``` and minio can be accessed at ```https:/localhost:8002```.

![](docs/assets/docker_start.png)

To double check if the server is up and running successfully running ```docker ps``` in the terminal lists the running containers, and we should see something like this:
```angular2html
CONTAINER ID   IMAGE                                      COMMAND                  CREATED             STATUS                       PORTS                                        NAMES
3d51a7580b6f   mlflow_nginx                               "nginx -g 'daemon of…"   About an hour ago   Up About an hour             0.0.0.0:80->80/tcp, 0.0.0.0:8002->8002/tcp   mlflow_nginx
1baa8ff12814   mlflow_app                                 "mlflow server --bac…"   About an hour ago   Up About an hour             5000/tcp                                     mlflow_server
a397b4149c5f   minio/minio:RELEASE.2021-03-17T02-33-02Z   "/usr/bin/docker-ent…"   About an hour ago   Up About an hour (healthy)   9000/tcp, 9002/tcp                           mlflow_server_s3_1
65374369fe4d   postgres:13.1                              "/docker-entrypoint.…"   About an hour ago   Up About an hour (healthy)   5432/tcp,                                    mlflow_db
```

<!-- Usage -->
## Overview

### Server components overview
When we ran ```docker-compose up``` we started 4 networked containers, each of which serves a purpose within the MLOps framework.
1. **NGINX**: The nginx container acts as a reverse proxy to control network traffic.
2. **MLflow**: The MLflow container hosts our MLflow server instance. This server is responsible for tracking and logging the MLOps events sent to it.
3. **MINIO**: The MINIO container hosts our MINIO server. Here we are using MINIO as a self hosted S3 storage location. The MLflow container interfaces well with S3 storage locations for logging artifacts (models, images, plots etc)
4. **postgres**: The database server container is visible only to the MLflow container, which logs MLflow entities to the postgres database hosted on this container. MLFlow entities should not be confused with artifacts (stored on MINIO), and are simple values such as metrics, parameters and configuration options which can be efficiently stored in a database.

There are two [bridge networks](https://docs.docker.com/network/bridge/) which connect these containers, named 'frontend' and 'backend'. The backend is used for communication between containers and is not accessible from the host (or remote), the frontend is accesible from the host (or remote) through the NGINX reverse proxy. NGINX will act as our gatekeeper and all requests will pass through it. This enables us to take advantage of NGINX load balancing and authentication in production versions.

### Experiment tracking with MLflow
MLflow is a framework for managing the full lifecycle of AI models. It contains tools to cover each stage of AI model lifecycle it contains 4 major component Tracking, Projects, Models, and a Model Registry. The endpoint for these tools is an MLflow server that cun run on local or remote hardware and handles all aspects of the lifecycle.

Currently, we will focus primarily on the tracking and projects components.

* Tracking refers to tools used to track experiments to record and compare parameters and results. This is done by adding logging snippets to the ML code to record things like hyper-parameters, metrics and artifacts. These entities are then associated with a particular run with a specific git commit. This git commit points to a specific version of the project files. This means that by using MLflow tracking we are able to identifiy the code used to train an AI model and make comparisons following changes to code structure and hyperparameter choices.

* MLflow uses projects to encapsulate AI tools in a reusable and reproducible way, based primarily on conventions. It also enables us to chain together project workflows meaning we are able to automate a great deal of the model development process.

### XNAT data integrations
Accessing data stored in an XNAT archive is performed through two steps.

#### 1. Create list of data samples
A list of subjects is extracted from the XNAT archive for the specified project. This is done automatically by the helper function `xnat_build_dataset`. 
```python
from mlops.data.tools.tools import xnat_build_dataset

PROJECT_ID = 'my_project'
xnat_configuration = {'server': XNAT_LOCATION,
                      'user': XNAT_USER,
                      'password': XNAT_USER_PASSWORD,
                      'project': XNAT_PROJECT_ID}

xnat_data_list = xnat_build_dataset(self.xnat_configuration)
``` 
Each element in the list `xnat_data_list` is a dictionary with two keys, Where these fields indicated unique references to each subject. 
```
{
    'subject_id': <subject_id>,
    'subject_uri': <subject_uri>
}
```
#### 2. Download relevant data using LoadImageXNATd and actions
A MONAI transform `LoadImageXNATd` is used to download the data from XNAT, this transform can be used in place of the conventional `LoadImaged` transform provided by MONAI to access local data.

A worked example is given below to create a valid dataloader containing the sag_t2_tse scans from XNAT where each subject has two experiments
This first thing that is required is an action function. This is a function that operates on an XNAT SubjectData object and returns the desired ImageScanData object from the archive and the key under which is will be stored in the dataset. For example the function below will extract the 'sag_t2_tse' scans from the archive.

```python
def fetch_sag_t2_tse(subject_data: SubjectData = None) -> (ImageScanData, str):
    """
    Function that identifies and returns the required xnat ImageData object from a xnat SubjectData object
    along with the 'key' that it will be used to access it.
    """
    for exp in subject_data.experiments:
        if 'MR_2' in subject_data.experiments[exp].label:
            for scan in subject_data.experiments[exp].scans:
                if 'sag_t2_tse' in subject_data.experiments[exp].scans[scan].series_description:
                    return subject_data.experiments[exp].scans[scan], 'sag_t2_tse'
```

In this example, the `fetch_sag_t2_tse` function will loop over all experiments available for the subject, then if one of these experiments has 'MR_2' in the label it will loop over all the scans in this experiment until it finds one with 'sag_t2_tse' in the series_description. The uri to this scan is then extracted and returned along with the key it will be stored under in the data dictionary, in this case 'sag_t2_tse'. 

We can now pass this action function to the `LoadImageXNATd` transform. When passing a list of action functions to the `LoadImageXNATd` transform each action function in the list will be performed sequentially. So if multiple datasets are required for each Subject then multiple functions can be used. 

```python
from mlops.data.transforms.LoadImageXNATd import LoadImageXNATd
from monai.transforms import Compose, ToTensord
from torch.utils.data import DataLoader
from monai.data import CacheDataset
from xnat.mixin import ImageScanData, SubjectData
from monai.data.utils import list_data_collate

# list of actions to be applied sequentially
actions = [fetch_sag_t2_tse]

train_transforms = Compose(
    [
        LoadImageXNATd(keys=['subject_uri'], actions=actions, xnat_configuration=xnat_configuration),
        ToTensord(keys=['sag_t2_tse'])
    ]
)

dataset = CacheDataset(data=xnat_data_list, transform=train_transforms)
data_loader = DataLoader(dataset, batch_size=1, shuffle=True, num_workers=0, collate_fn=list_data_collate)
```

If further transforms are required they can be added to the `Compose` transform list as usual.

<!-- tools -->
## Tools
Additional tools designed to be used with MLOps are located in the tools folder. 

Current tools:
datatoolkit

<!-- ROADMAP -->
## Roadmap
See the [open issues](https://github.com/GSTT-CSC/MLOps/issues) for a list of proposed features (and known issues).

<!-- CONTACT -->
## Contact

Laurence Jackson (GSTT-CSC)

Project Link: [https://github.com/GSTT-CSC/MLOps](https://github.com/GSTT-CSC/MLOps)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [README template by othneildrew](https://github.com/othneildrew/Best-README-Template)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/github_username

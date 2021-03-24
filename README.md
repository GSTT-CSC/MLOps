<!-- PROJECT HEADING -->
<br />
<p align="center">
<h3 align="center">MLOps</h3>

<p align="center">
A continuous integration and deployment framework for healthcare AI projects
<br />
<a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
<br />
<br />
<a href="https://github.com/GSTT-CSC/MLOps">View Demo</a>
·
<a href="https://github.com/GSTT-CSC/MLOps/issues">Report Bug</a>
·
<a href="https://github.com/GSTT-CSC/MLOps/issues">Request Feature</a>
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
    <li>
      <a href="#getting-started">Getting Started On Local Hardware</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#overview">Overview</a></li>
   <li><a href="#bringing-it-all-together:-hyper-parameter-tuning">Bringing it all together: hyper-parameter tuning</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
   <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project aims to build an effective MLOps framework for the development of AI models in a healthcare setting. 

If you want to get straight to it with an end to end example, see the [hyper-parameter tuning tutorial]().

### Open source components

* [DVC](https://dvc.org/) Data version control
* [MLflow](https://mlflow.org/) Open source platform to manage the ML lifecycle
* [MONAI](https://monai.io/) PyTorch-based framework for deep learning in healthcare imaging
* [MINIO](https://min.io/) High performance object storage suite
* [NGINX](https://www.nginx.com/) Reverse proxy server

It's not essential to have a complete understanding of all of these, but a high-level understanding of [MLflow](https://mlflow.org/) and [DVC](https://dvc.org/) in particular will be useful!

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
   ```
2. Navigate to the cloned code repository and start the server. Any docker images that are not present on your local system will be pulled from dockerhub (which might take a while).
    ```sh
   cd mlflow_server
   docker-compose up -d --build
   ```

<!-- Usage -->
## Overview

### Components overview
Opening a terminal and running ```docker ps``` lists the running containers, we should see something like this:
```angular2html
CONTAINER ID   IMAGE                                      COMMAND                  CREATED             STATUS                       PORTS                                        NAMES
3d51a7580b6f   mlflow_nginx                               "nginx -g 'daemon of…"   About an hour ago   Up About an hour             0.0.0.0:80->80/tcp, 0.0.0.0:8002->8002/tcp   mlflow_nginx
1baa8ff12814   mlflow_app                                 "mlflow server --bac…"   About an hour ago   Up About an hour             5000/tcp                                     mlflow_server
a397b4149c5f   minio/minio:RELEASE.2021-03-17T02-33-02Z   "/usr/bin/docker-ent…"   About an hour ago   Up About an hour (healthy)   9000/tcp, 9002/tcp                           mlflow_server_s3_1
65374369fe4d   mysql/mysql-server:5.7.28                  "/entrypoint.sh mysq…"   About an hour ago   Up About an hour (healthy)   3306/tcp, 33060/tcp                          mlflow_db
```
When we ran ```docker-compose up``` we started 4 networked containers, each of which serves a purpose within the MLOps framework.
1. **NGINX**: The nginx container acts as a reverse proxy to control network traffic.
2. **MLflow**: The MLflow container hosts our MLflow server instance. This server is responsible for tracking and logging the MLOps events sent to it.
3. **MINIO**: The MINIO container hosts our MINIO server. Here we are using MINIO as a self hosted S3 storage location. The MLflow container interfaces well with S3 storage locations for logging artifacts (models, images, plots etc)
4. **mysql**: The mysql server container is visible only to the MLflow container, which logs MLflow entities to the mysql database hosted on this container. MLFlow entities should not be confused with artifacts (stored on MINIO), and are simple values such as metrics, parameters and configuration options which can be efficiently stored in a database.

There are two [bridge networks](https://docs.docker.com/network/bridge/) which connect these containers, named 'frontend' and 'backend'. The backend is used for communication between containers and is not accessible from the host (or remote), the frontend is accesible from the host (or remote) through the NGINX reverse proxy. NGINX will act as our gatekeeper and all requests will pass through it. This enables us to take advantage of NGINX load balancing and authentication in production versions.

### Data versioning with DVC
AI projects differ from conventional software projects in that their results depend not only on the code used at runtime, but also on the data used to train the model. We can easily track code versions using git, and [we can use DVC in a similar way to track data](https://www.youtube.com/watch?v=UbL7VUpv1Bs). 
In brief, git is not intended to be used for large files, by using DVC we can track the version of data we use for a specific git commit and log the location of this data to a git repository. We only stored the data version and location, the data itself is stored elsewhere. 

### Experiment tracking with MLflow
MLflow is a framework for managing the full lifecycle of AI models. It contains tools to cover each stage of AI model lifecycle it contains 4 major component Tracking, Projects, Models, and a Model Registry. The endpoint for these tools is an MLflow server that cun run on local or remote hardware and handles all aspects of the lifecycle.

Currently, we will focus primarily on the tracking and projects components.

* Tracking refers to tools used to track experiments to record and compare parameters and results. This is done by adding logging snippets to the ML code to record things like hyper-parameters, metrics and artifacts. These entities are then associated with a particular run with a specific git commit. This git commit points to a specific version of the project files, which points to specific data version through DVC. This means that by using MLflow tracking we are able to identifiy the code and data versions used to train an AI model and make comparisons following changes to either.

* MLflow uses projects to encapsulate AI tools in a reusable and reproducible way, based primarily on conventions. It also enables us to chain together project workflows meaning we are able to automate a great deal of the model development process.

<!-- Bringing it all together: hyper-parameter tuning -->
## Bringing it all together: hyper-parameter tuning

-----
Seeing each of these components independatly is useful but the best way to learn how all these comoponets work together is with an example. Almost all AI models will benefit from the process of hyper parameter tuning, a process which is difficult when attempted without a robust MLOps service. This example demonstrates how using the experiment tracking described above facilitates this process.

For a detailed tutorial describing the end-to-end process of AI development using this framework please see the following blog post.

#### [Hyper-parameter tuning tutorial](https://gstt-csc.github.io/) 


<!-- ROADMAP -->
## Roadmap
See the [open issues](https://github.com/GSTT-CSC/MLOps/issues) for a list of proposed features (and known issues).


<!-- CONTRIBUTING -->
## Contributing
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- CONTACT -->
## Contact

-----
Laurence Jackson (GSTT-CSC)

Project Link: [https://github.com/GSTT-CSC/MLOps](https://github.com/GSTT-CSC/MLOps)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

-----

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

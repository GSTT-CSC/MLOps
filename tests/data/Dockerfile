FROM python:3.9
RUN apt-get update && apt-get install -y git

# Configure application
ADD requirements.txt .
RUN python3 -m pip install --upgrade pip && python3 -m pip install --ignore-installed ruamel-yaml -r requirements.txt

# Setup MLOps
RUN git clone --branch feature/mlflow_server https://github.com/GSTT-CSC/MLOps.git
RUN python3 -m pip install --ignore-installed ruamel-yaml -r MLOps/requirements.txt \
    && python3 -m pip install MLOps/

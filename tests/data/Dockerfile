FROM pytorch/pytorch:1.7.1-cuda11.0-cudnn8-runtime
RUN apt-get update && apt-get install -y build-essential git ffmpeg libsm6 libxext6

# Configure application
ADD requirements.txt .
RUN python3 -m pip install --upgrade pip && python3 -m pip install --ignore-installed ruamel-yaml -r requirements.txt

# Setup MLOps
RUN git clone --branch feature/mlflow_server https://github.com/GSTT-CSC/MLOps.git
RUN python3 -m pip install --ignore-installed ruamel-yaml -r MLOps/requirements.txt \
    && python3 -m pip install MLOps/

FROM python:3.9-slim
RUN apt-get update && apt-get install -y git

# Configure application
COPY . .

RUN python3 -m pip install --upgrade pip && python3 -m pip install --ignore-installed ruamel-yaml -r requirements.txt

## Setup MLOps
#RUN python setup.py install

WORKDIR /tests/data
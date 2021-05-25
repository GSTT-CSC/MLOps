# Dockerfile for configuring mlflow test_project container

FROM python:3.8
ADD requirements.txt .
#Configure app
RUN pip install --no-cache-dir -r requirements.txt

# docker build -t mlflow-docker-test -f Dockerfile .
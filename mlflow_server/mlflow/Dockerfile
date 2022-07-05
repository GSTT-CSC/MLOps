FROM python:3.8-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Installing packages
RUN apt-get update && apt-get -y install libpq-dev gcc
RUN pip install --upgrade pip && pip install mlflow==1.26.0 psycopg2 psycopg2-binary sqlalchemy pymysql boto3 torch-model-archiver torchserve mlflow-torchserve
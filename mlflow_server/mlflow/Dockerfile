FROM python:3.8-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Installing packages
RUN apt-get update && apt-get -y install libpq-dev gcc
RUN pip install --upgrade pip && pip install mlflow psycopg2 psycopg2-binary sqlalchemy pymysql boto3 torch-model-archiver torchserve mlflow-torchserve protobuf~=3.19.0 # protobuf is temporary solution to avoid breaking changes made to 3rd party streamlit (necessary for mlflow) https://discuss.streamlit.io/t/typeerror-descriptors-cannot-not-be-created-directly/25639
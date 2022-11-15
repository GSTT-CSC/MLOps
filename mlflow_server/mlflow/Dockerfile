FROM python:3.9-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Installing packages
RUN apt-get update && apt-get -y install libpq-dev gcc
COPY requirements_mlflow.txt requirements_mlflow.txt
RUN pip install --upgrade pip && pip install -r requirements_mlflow.txt
FROM python:3.9-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV MLFLOW_HTTP_REQUEST_TIMEOUT=500

# Installing packages
RUN apt-get update && apt-get -y install libpq-dev gcc build-essential
COPY requirements_mlflow.txt requirements_mlflow.txt
RUN pip install --upgrade pip && pip install -r requirements_mlflow.txt
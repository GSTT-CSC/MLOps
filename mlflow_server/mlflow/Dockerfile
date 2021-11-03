FROM python:3.8-slim

# Installing packages
RUN apt-get update && apt-get -y install libpq-dev gcc

RUN pip install mlflow[extras] psycopg2 psycopg2-binary sqlalchemy pymysql boto3
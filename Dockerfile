FROM python:3.8

# Configure container
#RUN groupadd -r user && useradd --create-home --shell /bin/bash -r -g user user
#RUN mkdir /home/user/workspace
#RUN mkdir /home/user/app
#ADD requirements.txt /home/user/app
ADD requirements.txt .
#WORKDIR /home/user/app
EXPOSE 5000

#Configure app
RUN pip install --no-cache-dir -r requirements.txt

#USER user
#WORKDIR /home/user/workspace

# check this out - need to work out how to expose server to container
# https://blog.noodle.ai/introduction-to-mlflow-for-mlops-part-2-docker-environment/
#and part 2:
# https://blog.noodle.ai/introduction-to-mlflow-for-mlops-part-3-database-tracking-minio-artifact-storage-and-registry/

# another useful mlflow guide
#https://docs.microsoft.com/en-us/azure/databricks/applications/mlflow/model-registry-example
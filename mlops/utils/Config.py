import configparser
import logging
import os

logger = logging.getLogger(__name__)


class Config:

    def __init__(self, config_path):
        self.config_path = config_path

    def parse_config(self):
        logger.info('reading config file: {0}'.format(self.config_path))
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)

        # if mlflow reserved variables are already present in env use them
        if os.getenv('MLFLOW_TRACKING_URI'):
            self.config['server']['MLFLOW_TRACKING_URI'] = os.getenv('MLFLOW_TRACKING_URI')
        if os.getenv('MLFLOW_S3_ENDPOINT_URL'):
            self.config['server']['MLFLOW_S3_ENDPOINT_URL'] = os.getenv('MLFLOW_S3_ENDPOINT_URL')
        if os.getenv('ARTIFACT_PATH'):
            self.config['server']['ARTIFACT_PATH'] = os.getenv('ARTIFACT_PATH')

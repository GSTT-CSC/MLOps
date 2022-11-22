"""
ProjectFile
"""
import yaml
import datetime
import os
from mlops.utils.logger import logger


class ProjectFile:

    def __init__(self, config, config_path, script, path: str = '.', projectfile_name: str = 'MLproject',
                 clean_projectfile: bool = True) -> None:
        """
        Uses the MLOps configurations to create an MLproject file used my mlflow to define the project.

        This class processes the config object that is inputted and converts it to a project_dict dictionary. This dict
        is then used to create the MLproject yaml file.

        :param config: ConfigParser object
        :param path: path to the project directory
        :param projectfile_name: name of project file, this should not need to be changed if mlflow is the target
        :param clean_projectfile: bool flag to indicate whether to regenerate the project file on each run (recommend keeping this True)
        """
        self.config_path = config_path
        self.config = config
        self.projectfile_name = projectfile_name
        self.project_path = os.path.join(path, projectfile_name)

        # Clean projectfile if it exists
        if clean_projectfile and os.path.exists(self.project_path):
            logger.debug('Removing existing project file: {0}'.format(self.project_path))
            os.remove(os.path.join(path, self.projectfile_name))

        docker_env = {'image': config['project']['NAME'].lower(),
                      'environment': ["PYTHONPATH"]}

        if config.has_option('project', 'VOLUME_MOUNT'):
            docker_env['volumes'] = [config['project']['VOLUME_MOUNT']]

        self.project_dict = {
            'name': config['project']['NAME'].lower(), 'docker_env': docker_env,
            'entry_points': {'main': {'command': ' '.join(['python3', script, self.config_path])
                                      }
                             }
        }

    def generate_yaml(self):
        """
        Creates yaml projectfile from collected project_dict
        :return:
        """
        logger.info('Writing project file: {0}'.format(self.project_path))
        with open(self.project_path, 'w+') as f:
            f.write('# {0}: This ProjectFile was automatically generated by MLOps\n\n'.format(datetime.datetime.now()))
            yaml.dump(self.project_dict, f, default_flow_style=False, sort_keys=False)

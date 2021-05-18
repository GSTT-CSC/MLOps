"""
ProjectFile
"""
import yaml
import datetime


class ProjectFile:

    def __init__(self, config, projectfile_name='MLProject'):
        self.config = config
        self.projectfile_name = projectfile_name
        self.project_dict = {'name': config['project']['NAME'],
                             'docker_env': {'volumes': [config['project']['VOLUME_MOUNT']],
                                            'image': config['project']['NAME']}}

        self._parse_entry_points()

    def _parse_entry_points(self):
        entry_points_dict = {}
        for key in self.config['entry_points']:
            entry_points_dict[key] = {'command': self.config['entry_points'][key]}
        self.project_dict['entry_points'] = entry_points_dict

    def generate_yaml(self):
        with open(self.projectfile_name, 'w+') as f:
            f.write('# {0} : This ProjectFile was automatically generated by MLOps\n\n'.format(datetime.datetime.now()))
            yaml.dump(self.project_dict, f, default_flow_style=False, sort_keys=False)

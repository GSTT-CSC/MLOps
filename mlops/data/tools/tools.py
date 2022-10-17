import xnat
from mlops.utils.logger import logger
from itertools import chain


def xnat_build_dataset(xnat_configuration: dict, actions: list = None, flatten_output=True):
    """
    Builds a dictionary that describes the XNAT project dataset using XNAT data hierarchy: project/subject/experiment/scan

    structured output returned flattened dataset. Can set structured_output to True to perform custom flattening.

    """

    with xnat.connect(server=xnat_configuration['server'],
                      user=xnat_configuration['user'],
                      password=xnat_configuration['password'],
                      verify=xnat_configuration['verify'],
                      ) as session:

        logger.info(f"Collecting XNAT project: {xnat_configuration['project']}")
        project = session.projects[xnat_configuration["project"]]

        dataset = []
        for subject in project.subjects:

            data_sample = {'subject_uri': project.subjects[subject].uri,
                           'subject_id': project.subjects[subject].label,
                           'data': []}

            if actions:
                try:
                    data = []
                    for action, data_label in actions:
                        action_data = []
                        #  No actions, just return a list of subject IDs and URIs
                        logger.debug(f"Running action: {action.__name__} on {subject}")
                        xnat_obj = action(project.subjects[subject])

                        if len(xnat_obj) == 0:
                            raise Exception

                        for obj in xnat_obj:
                            action_data.append({'source_action': action.__name__,
                                                'xnat_uri': obj.uri,
                                                'data_label': data_label})

                        data.append(action_data)

                except:
                    logger.warn('No data found; removing sample.')
                    continue

                if flatten_output:
                    data = list(chain(*data))

                data_sample['data'] = data

            dataset.append((data_sample))

    return dataset

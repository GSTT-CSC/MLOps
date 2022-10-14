import xnat
from mlops.utils.logger import logger
from itertools import chain


def xnat_build_dataset(xnat_configuration: dict, actions: list = None, structured_output: bool = False):
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
            data_series = []
            if actions:
                for action, data_label in actions:
                    try:
                        #  No actions, just return a list of subject IDs and URIs
                        logger.debug(f"Running action: {action.__name__} on {subject}")
                        xnat_obj = action(project.subjects[subject])
                        output = []
                        for obj in xnat_obj:
                            output.append({'source_action': action.__name__,
                                           'xnat_uri': obj.uri,
                                           'data_label': data_label,
                                           'subject_uri': project.subjects[subject].uri,
                                           'subject_id': project.subjects[subject].label})
                        if output:
                            dataset.append(output)
                        else:
                            logger.warn(f'No suitable data found, ignoring sample')
                            continue
                    except TypeError:
                        logger.warn(f'No suitable data found, ignoring sample')
                        continue
            else:
                #  No actions, just return a list of subject IDs and URIs
                data_series.append({'subject_uri': project.subjects[subject].uri})
                dataset.append(data_series)

    if not structured_output:
        return list(chain(*dataset))
    else:
        return dataset

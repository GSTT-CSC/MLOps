import xnat
from mlops.utils.logger import logger


def xnat_build_dataset(xnat_configuration: dict, actions: list = None):
    """
    Builds a dictionary that describes the XNAT project dataset using XNAT data hierarchy: project/subject/experiment/scan

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
                    #  No actions, just return a list of subject IDs and URIs
                    data_series
                    logger.debug(f"Running action: {action.__name__} on {subject}")
                    s = project.subjects[subject]
                    try:
                        xnat_obj = action(project.subjects[subject])
                        output = []
                        for obj in xnat_obj:
                            output.append({'source_action': action.__name__,
                                           'xnat_uri': obj.uri,
                                           'data_label': data_label,
                                           'subject_uri': project.subjects[subject].uri})
                        dataset.append(output)
                    except TypeError:
                        logger.warn(f'No suitable data found for action {action} and subject {d["subject_uri"]}')
                        xnat_obj = None
                        # todo: work out how to remove this data from the dataset

            else:
                #  No actions, just return a list of subject IDs and URIs
                data_series['subject_uri'] = project.subjects[subject].uri
                dataset.append(data_series)

    return dataset

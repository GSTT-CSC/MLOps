import xnat
from mlops.utils.logger import logger
from itertools import chain
import mlflow
import pandas as pd


def xnat_build_dataset(xnat_configuration: dict, actions: list = None, flatten_output=True, test_batch: int = -1):
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

        if 0 < test_batch < len(project.subjects):
            from random import sample
            project_subjects = sample(project.subjects[:], test_batch)
        else:
            project_subjects = project.subjects[:]

        missing_data_log = []
        for subject_i in project_subjects:
            subject = project.subjects.data[subject_i.id]
            data_sample = {'subject_uri': project.subjects[subject.id].uri,
                           'subject_id': project.subjects[subject.id].label,
                           'data': []}

            if actions:
                try:
                    data = []
                    for action, data_label in actions:
                        action_data = []

                        logger.debug(f"Running action: {action.__name__} on {subject.id}")
                        xnat_obj = action(project.subjects[subject.id])

                        if type(xnat_obj) == list:
                            if len(xnat_obj) == 0:
                                missing_data_log.append({'subject_id': subject_i.id,
                                                         'action_data': subject_i.label,
                                                         'failed_action': action})
                                logger.warn(f'No data found for {subject_i}: action {action} removing sample')
                                raise Exception

                            for obj in xnat_obj:
                                action_data.append({'source_action': action.__name__,
                                                    'action_data': obj.uri,
                                                    'data_type': 'xnat_uri',
                                                    'data_label': data_label})
                        elif type(xnat_obj) == str:
                            action_data.append({'source_action': action.__name__,
                                                'action_data': xnat_obj,
                                                'data_type': 'value',
                                                'data_label': data_label})

                        data.append(action_data)

                except Exception as e:
                    logger.warn(f'No data found for {subject_i}; removing sample. Exception {e}')
                    continue

                if flatten_output:
                    data = list(chain(*data))

                data_sample['data'] = data

            dataset.append((data_sample))

        if missing_data_log:
            df = pd.DataFrame(missing_data_log)
            df.to_csv('missing_data_log.csv')
            mlflow.log_artifact('missing_data_log.csv')
            mlflow.log_param('N_failed_xnat_samples', len(df))

    return dataset

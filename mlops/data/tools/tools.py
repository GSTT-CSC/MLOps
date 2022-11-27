import xnat
from mlops.utils.logger import logger
from itertools import chain
import mlflow
import pandas as pd

import xnat
from mlops.utils.logger import logger
from itertools import chain
import mlflow
import pandas as pd
import requests
import asyncio
from timeit import default_timer
from concurrent.futures import ThreadPoolExecutor


class DataBuilderXNAT:

    def __init__(self, xnat_configuration: dict, actions: list = None, flatten_output=True, test_batch: int = -1,
                 num_workers: int = 1):
        self.xnat_configuration = xnat_configuration
        self.actions = actions
        self.flatten_output = flatten_output
        self.test_batch = test_batch
        self.missing_data_log = []
        self.num_workers = num_workers

        self.dataset = []

    def fetch_data(self):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.start_async_process())
        loop.run_until_complete(future)

    async def start_async_process(self):
        with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            # with requests.Session() as session:
            with xnat.connect(server=self.xnat_configuration['server'],
                              user=self.xnat_configuration['user'],
                              password=self.xnat_configuration['password'],
                              verify=self.xnat_configuration['verify'],
                              ) as session:

                logger.info(f"Collecting XNAT project: {self.xnat_configuration['project']}")
                project = session.projects[self.xnat_configuration["project"]]

                dataset = []

                if 0 < self.test_batch < len(project.subjects):
                    from random import sample
                    project_subjects = sample(project.subjects[:], self.test_batch)
                else:
                    project_subjects = project.subjects[:]

                loop = asyncio.get_event_loop()
                tasks = [
                    loop.run_in_executor(
                        executor,
                        self.process_subject,
                        *(project, subject_i)
                    )
                    for subject_i in project_subjects
                ]
                for response in await asyncio.gather(*tasks):
                    pass

                # remove any items where not all actions returned a value
                self.dataset = [item for item in self.dataset if len(item['data']) == len(self.actions)]

    def process_subject(self, project, subject_i):
        subject = project.subjects.data[subject_i.id]
        data_sample = {'subject_uri': project.subjects[subject.id].uri,
                       'subject_id': project.subjects[subject.id].label,
                       'data': []}

        logger.info(f'checking subject {subject_i}')

        if self.actions:
            try:
                data = []
                for action, data_label in self.actions:
                    action_data = []

                    # logger.debug(f"Running action: {action.__name__} on {subject.id}")
                    xnat_obj = action(project.subjects[subject.id])

                    if type(xnat_obj) == list:
                        if len(xnat_obj) == 0:
                            self.missing_data_log.append({'subject_id': subject_i.id,
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
                pass

            if self.flatten_output:
                data = list(chain(*data))

            data_sample['data'] = data

        self.dataset.append((data_sample))


def xnat_build_dataset(xnat_configuration: dict, actions: list = None, flatten_output=True, test_batch: int = -1):
    """
    ***NOTE THE ASYNC VERSION ABOVE WILL BE MUCH FASTER FOR LARGE DATASETS***

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

                        # logger.debug(f"Running action: {action.__name__} on {subject.id}")
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

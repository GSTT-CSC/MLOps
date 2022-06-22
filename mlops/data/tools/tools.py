import xnat
from mlops.utils.logger import logger


def xnat_build_dataset(xnat_configuration: dict = None, minimal: bool = True):
    """
    Builds a dictionary that describes the XNAT project dataset using XNAT data hierarchy: project/subject/experiment/scan

    minimal: if True, only the minimal information is returned, i.e. the  subject ID and the SubjectData

    e.g.
    [
        {
        subjectid: '1',
        subject_uri: '<unique address to subject in xnat archive>'
        experiment_1: {
                        scan_1: {scan_object},
                        scan_2: {scan_object}
                       },
        experiment_2:  {
                        scan_1: {scan_object}
                      }
        }
    ]

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

            data_series = {'subject_id': project.subjects[subject].label, 'subject_uri': project.subjects[subject].uri}

            if not minimal:
                for experiment in project.subjects[subject].experiments:
                    scan_dict = {}
                    for scan in project.subjects[subject].experiments[experiment].scans:
                        scan_dict['modality'] = project.subjects[subject].experiments[experiment].modality
                        scan_dict[project.subjects[subject].experiments[experiment].scans[scan].series_description] = project.subjects[subject].experiments[experiment].scans[scan]

                    data_series[project.subjects[subject].experiments[experiment].label] = scan_dict
            logger.debug(f"Adding data series to dataset: {data_series}")
            dataset.append(data_series)

    return dataset


import xnat


def xnat_build_dataset(xnat_configuration, minimal=True):
    """
    Builds a dictionary that describes the XNAT project dataset using XNAT data hierarchy: project/subject/experiment/scan

    minimal: if True, only the minimal information is returned, i.e. the  subject ID and the SubjectData

    e.g.
    [
        {
        subject_id: '1',
        experiments:    {
                        experiment_1: {
                                        scan_1: {scan_object},
                                        scan_2: {scan_object}
                                       },
                        experiment_2:  {
                                        scan_1: {scan_object}
                                      }
                        },
        }

        {
        subject: '2',
        ...,
        }
    ]

    """
    with xnat.connect(server=xnat_configuration['server'],
                      user=xnat_configuration['user'],
                      password=xnat_configuration['password']) as session:

        project = session.projects[xnat_configuration["project"]]

        dataset = []
        for subject in project.subjects:
            data_series = {}
            data_series['subject_id'] = subject
            data_series['subject_uri'] = project.subjects[subject].uri
            experiment_dict = {}
            if not minimal:
                for experiment in project.subjects[subject].experiments:
                    scan_dict = {}
                    for scan in project.subjects[subject].experiments[experiment].scans:
                        scan_dict['modality'] = project.subjects[subject].experiments[experiment].modality
                        scan_dict[project.subjects[subject].experiments[experiment].scans[scan].series_description] = project.subjects[subject].experiments[experiment].scans[scan]

                    data_series[project.subjects[subject].experiments[experiment].label] = scan_dict

            dataset.append(data_series)

    return dataset


"""
MONAI MapTransform for importing image data from XNAT
"""
import tempfile
import xnat
import os
import glob
from monai.transforms import MapTransform, LoadImage
from monai.config import KeysCollection
from mlops.utils.logger import logger


class LoadImageXNATd(MapTransform):
    """
    MapTransform for importing image data from XNAT
    """

    def __init__(self, keys: KeysCollection, xnat_configuration=None, image_loader=LoadImage):
        super().__init__(keys)
        self.image_loader = image_loader
        self.xnat_configuration = xnat_configuration

    def __call__(self, data):
        d = dict(data)
        for key in self.keys:
            if key in data:

                with xnat.connect(server=self.xnat_configuration['server'],
                                  user=self.xnat_configuration['user'],
                                  password=self.xnat_configuration['password'], ) as session:

                    "XNAT data hierarchy: project/subject/experiment/scan"
                    project = session.projects[self.xnat_configuration["project"]]
                    subject = project.subjects[str(d[key])]

                    "Raise exception to >1 experiment. This is not currently supported"
                    if len(subject.experiments) == 1:
                        experiment = subject.experiments[0]
                    else:
                        raise ValueError("XNAT subject has more than one experiment")

                    for scan in experiment.scans.items():
                        with tempfile.TemporaryDirectory() as tmpdirname:
                            logger.debug('Downloading {project}/{subject}/{experiment}/{scan}'.
                                         format(project=project,
                                                subject=subject,
                                                experiment=experiment,
                                                scan=scan))

                            experiment.scans[scan[0]].download_dir(tmpdirname)
                            images_path = glob.glob(os.path.join(tmpdirname, '**/*.dcm'), recursive=True)
                            image, meta = self.image_loader()(images_path)

                            d['image'] = image
                            d['meta'] = meta

                return d

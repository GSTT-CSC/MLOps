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

    def __init__(self, keys: KeysCollection, actions=None, xnat_configuration=None, image_loader=LoadImage, validate_data:bool = False, expected_filetype='.dcm'):
        super().__init__(keys)
        self.image_loader = image_loader
        self.xnat_configuration = xnat_configuration
        self.actions = actions
        self.expected_filetype = expected_filetype
        self.validate_data = validate_data

    def __call__(self, data):
        d = dict(data)
        for key in self.keys:
            if key in data:

                for action, data_label in self.actions:
                    """loops over actions in action list, if no action is triggered then raise a warning actions are 
                    functions that return any of projects, subjects, experiments, scans, or resources XNAT object 
                    along with a key to be used in the data dictionary"""

                    logger.debug(f"Running XNAT action: {action}")

                    with xnat.connect(server=self.xnat_configuration['server'],
                                      user=self.xnat_configuration['user'],
                                      password=self.xnat_configuration['password'], loglevel='INFO', logger=logger, verify=bool(os.getenv('MLOPS_SSL'))) as session:

                        "connect session to subject uri"
                        subject_obj = session.create_object(d['subject_uri'])
                        "perform action on subject object"
                        try:
                            xnat_obj = action(subject_obj)
                        except TypeError:
                            logger.warn(f'No suitable data found for action {action} and subject {d["subject_uri"]}')
                            d[data_label] = None

                        if self.validate_data:
                            if xnat_obj:
                                d[data_label] = True
                            else:
                                d[data_label] = False
                            return d

                        with tempfile.TemporaryDirectory() as tmpdirname:
                            "download image from XNAT"
                            session_obj = session.create_object(xnat_obj.uri)
                            session_obj.download_dir(tmpdirname)

                            images_path = glob.glob(os.path.join(tmpdirname, '**/*' + self.expected_filetype), recursive=True)

                            "find unique directories in list of image paths"
                            image_dirs = list(set(os.path.dirname(image_path) for image_path in images_path))

                            if len(image_dirs) > 1:
                                raise ValueError(f'More than one image series found in {images_path}')

                            logger.info(f"Downloading image: {image_dirs[0]}")

                            image, meta = self.image_loader()(image_dirs[0])

                            d[data_label] = image
                            d[data_label + '_meta'] = meta

            return d

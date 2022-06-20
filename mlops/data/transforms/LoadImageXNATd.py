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
from monai.transforms.transform import Transform


class LoadImageXNATd(MapTransform):
    """
    MapTransform for importing image data from XNAT
    """

    def __init__(self, keys: KeysCollection, actions: list = None, xnat_configuration: dict = None,
                 image_loader: Transform = LoadImage, validate_data: bool = False, expected_filetype_ext: str = '.dcm'):
        super().__init__(keys)
        self.image_loader = image_loader
        self.xnat_configuration = xnat_configuration
        self.actions = actions
        self.expected_filetype = expected_filetype_ext
        self.validate_data = validate_data

    def __call__(self, data):
        """
        Checks for the requested keys in the input data dictionary.

        If specified key is found then will loop over actions in action list and apply each to the value of the
        requested key, if no action is triggered then raise a warning actions arefunctions that return any of projects,
        subjects, experiments, scans, or resources XNAT object along with a key to be used in the data dictionary

        Each action function should locate a single image object in XNAT. This image object is then downloaded to a
        temporary directory and loaded into memory as the value defined by key set by the actions' data_label.

        If validate_data is true then NO data will be downloaded. In this case the transform will loop over the actions
        but will instead return a true/false value for each data sample. This can be used to remove samples where the
        data is not present in XNAT.

        :param data: dictionary of data
        :return:
        """

        d = dict(data)

        for key in self.keys:

            if key in data:

                for action, data_label in self.actions:

                    logger.debug(f"Running XNAT action: {action}")

                    with xnat.connect(server=self.xnat_configuration['server'],
                                      user=self.xnat_configuration['user'],
                                      password=self.xnat_configuration['password'],
                                      verify=self.xnat_configuration['verify'],
                                      ) as session:

                        # "connect session to subject uri"
                        subject_obj = session.create_object(d['subject_uri'])
                        logger.debug(f"Found XNAT subject: {subject_obj}")

                        # perform action on subject object
                        try:
                            xnat_obj = action(subject_obj)
                            logger.debug(f"Running {action} found XNAT obj: {xnat_obj}")
                        except TypeError:
                            logger.warn(f'No suitable data found for action {action} and subject {d["subject_uri"]}')
                            xnat_obj = None

                        if self.validate_data:
                            if xnat_obj is not None:
                                d[data_label] = True
                                return d
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

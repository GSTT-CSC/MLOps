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
from monai.transforms import Transform


class LoadImageXNATd(MapTransform):
    """
    MapTransform for importing image data from XNAT
    """

    def __init__(self, keys: KeysCollection,  xnat_configuration: dict = None,
                 image_loader: Transform = LoadImage(), validate_data: bool = False, expected_filetype_ext: str = '.dcm'):
        super().__init__(keys)
        self.image_loader = image_loader
        self.xnat_configuration = xnat_configuration
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

                data_label = d['data_label']

                with xnat.connect(server=self.xnat_configuration['server'],
                                  user=self.xnat_configuration['user'],
                                  password=self.xnat_configuration['password'],
                                  verify=self.xnat_configuration['verify'],
                                  ) as session:

                    "Download image from XNAT"
                    with tempfile.TemporaryDirectory() as tmpdirname:
                        session_obj = session.create_object(d['xnat_uri'])
                        session_obj.download_dir(tmpdirname)

                        images_path = glob.glob(os.path.join(tmpdirname, '**/*' + self.expected_filetype), recursive=True)

                        # image loader needs full path to load single images
                        logger.info(f"Downloading images: {images_path}")
                        if len(images_path) == 1:
                            image, meta = self.image_loader(images_path)

                        # image loader needs directory path to load 3D images
                        else:
                            "find unique directories in list of image paths"
                            image_dirs = list(set(os.path.dirname(image_path) for image_path in images_path))
                            if len(image_dirs) > 1:
                                raise ValueError(f'More than one image series found in {images_path}')
                            image, meta = self.image_loader(image_dirs[0])

                        # data.append(image, meta)
                        d[data_label] = image
                        d[data_label + '_meta'] = meta

            return d

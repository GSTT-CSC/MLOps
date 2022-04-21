"""
MONAI MapTransform for importing image data from XNAT
"""
import tempfile
import xnat
import os
import glob
from monai.transforms import MapTransform, LoadImage
from monai.config import KeysCollection


class LoadImageXNATd(MapTransform):
    """
    MapTransform for importing image data from XNAT
    """

    def __init__(self, keys: KeysCollection, actions=None, xnat_configuration=None, image_loader=LoadImage, expected_filetype='.dcm'):
        super().__init__(keys)
        self.image_loader = image_loader
        self.xnat_configuration = xnat_configuration
        self.actions = actions
        self.expected_filetype = expected_filetype

    def __call__(self, data):
        d = dict(data)
        for key in self.keys:
            if key in data:

                for action in self.actions:
                    """loops over actions in action list, if no action is triggered then raise a warning actions are 
                    functions that return any of projects, subjects, experiments, scans, or resources XNAT object 
                    along with a key to be used in the data dictionary"""

                    with xnat.connect(server=self.xnat_configuration['server'],
                                      user=self.xnat_configuration['user'],
                                      password=self.xnat_configuration['password'], ) as session:

                        "connect session to subject uri"
                        subject_obj = session.create_object(d['subject_uri'])
                        "perform action on subject object"
                        xnat_obj, image_label = action(subject_obj)

                        with tempfile.TemporaryDirectory() as tmpdirname:
                            "download image from XNAT"
                            session_obj = session.create_object(xnat_obj.uri)
                            session_obj.download_dir(tmpdirname)

                            images_path = glob.glob(os.path.join(tmpdirname, '**/*' + self.expected_filetype), recursive=True)

                            "find unique directories in list of image paths"
                            image_dirs = list(set(os.path.dirname(image_path) for image_path in images_path))

                            if len(image_dirs) > 1:
                                raise ValueError(f'More than one image series found in {images_path}')

                            image, meta = self.image_loader()(image_dirs[0])

                            d[image_label] = image
                            d[image_label + '_meta'] = meta

            return d

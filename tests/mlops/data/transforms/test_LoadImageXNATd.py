import xnat
from mlops.data.transforms.LoadImageXNATd import LoadImageXNATd
from mlops.data.tools.tools import xnat_build_dataset
from monai.transforms import Compose, ToTensord
from torch.utils.data import DataLoader
from monai.data import CacheDataset
from xnat.mixin import ImageScanData, SubjectData
import requests
from xnat.exceptions import XNATUploadError
from requests.auth import HTTPBasicAuth


class TestLoadImageXNATd:

    def setup(self):
        self.test_batch_size = 1
        self.xnat_configuration = {'server': 'http://localhost',
                                   'user': 'admin',
                                   'password': 'admin',
                                   'project': 'TEST_MLOPS'}

        self.test_xnat_connection(self.xnat_configuration['server'])

        #  create test project and push test data
        with xnat.connect(server=self.xnat_configuration['server'],
                          user=self.xnat_configuration['user'],
                          password=self.xnat_configuration['password'], ) as session:

            xnat_projects_url = self.xnat_configuration['server'] + '/data/projects'

            # Set the name of the XML file.
            headers = {'Content-Type': 'text/xml'}

            # Open the XML file.
            with open('tests/data/xnat/test_project_setup.xml') as xml:
                r = requests.post(xnat_projects_url, data=xml, headers=headers,
                                  auth=HTTPBasicAuth(self.xnat_configuration['user'],
                                                     self.xnat_configuration['password']))

            # push data to new project
            try:
                session.services.import_('tests/data/test_dicoms.zip', project=self.xnat_configuration['project'],
                                         subject='1',
                                         experiment='MR_TEST_EXPERIMENT')
            except XNATUploadError:
                print('Test subject already exists')

        self.test_data = xnat_build_dataset(self.xnat_configuration)

    def test_xnat_connection(self, url):
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xxx
        except Exception as e:
            raise e
        else:
            print("All good!")  # Proceed to do stuff with `r`

    def test_create_dataloader_with_transform(self):

        def fetch_test_exp(subject_data: SubjectData = None) -> (ImageScanData, str):
            """
            Function that identifies and returns the required xnat ImageData object from a xnat SubjectData object
            along with the 'key' that it will be used to access it.
            """
            for exp in subject_data.experiments:
                if 'MR_TEST_EXPERIMENT' in subject_data.experiments[exp].label:
                    for scan in subject_data.experiments[exp].scans:
                        if 'SlicePosition' in subject_data.experiments[exp].scans[scan].series_description:
                            return subject_data.experiments[exp].scans[scan], 'test_image'

        # fetches are applied sequentially
        actions = [fetch_test_exp]

        self.train_transforms = Compose(
            [
                LoadImageXNATd(keys=['subject_uri'], actions=actions, xnat_configuration=self.xnat_configuration, expected_filetype='.IMA'),
                ToTensord(keys=['test_image'])
            ]
        )

        self.dataset = CacheDataset(data=self.test_data, transform=self.train_transforms)
        from monai.data.utils import list_data_collate
        self.loader = DataLoader(self.dataset, batch_size=self.test_batch_size,
                                 shuffle=True, num_workers=0, collate_fn=list_data_collate)

        for i_batch, sample_batched in enumerate(self.loader):
            assert 'test_image' in sample_batched
            assert len(sample_batched['test_image']) == self.test_batch_size

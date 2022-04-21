from mlops.data.transforms.LoadImageXNATd import LoadImageXNATd, cleankeysd
from mlops.data.tools.tools import xnat_build_dataset
from monai.transforms import Compose, ToTensord
from torch.utils.data import DataLoader
from monai.data import CacheDataset
from xnat.mixin import ImageScanData, SubjectData
from monai.data.utils import list_data_collate


class TestLoadImageXNATd:

    def setup(self):
        self.test_batch_size = 1
        self.xnat_configuration = {'server': 'http://localhost',
                                   'user': 'admin',
                                   'password': 'admin',
                                   'project': 'MLOPS002'}

        self.test_data = xnat_build_dataset(self.xnat_configuration)

    def test_get_data(self):

        def fetch_sag_t2_tse(subject_data: SubjectData = None) -> (ImageScanData, str):
            """
            Function that identifies and returns the required xnat ImageData object from a xnat SubjectData object
            along with the 'key' that it will be used to access it.
            """
            for exp in subject_data.experiments:
                if 'MR_2' in subject_data.experiments[exp].label:
                    for scan in subject_data.experiments[exp].scans:
                        if 'sag_t2_tse' in subject_data.experiments[exp].scans[scan].series_description:
                            return subject_data.experiments[exp].scans[scan], 'sag_t2_tse'

        # fetches are applied sequentially
        actions = [fetch_sag_t2_tse]

        self.train_transforms = Compose(
            [
                LoadImageXNATd(keys=['subject_uri'], actions=actions, xnat_configuration=self.xnat_configuration),
                ToTensord(keys=['sag_t2_tse'])
            ]
        )

        self.dataset = CacheDataset(data=self.test_data, transform=self.train_transforms)
        from monai.data.utils import list_data_collate
        self.loader = DataLoader(self.dataset, batch_size=self.test_batch_size,
                                 shuffle=True, num_workers=0, collate_fn=list_data_collate)

        for i_batch, sample_batched in enumerate(self.loader):
            assert len(sample_batched) == self.test_batch_size

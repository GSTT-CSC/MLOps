from mlops.data.transforms.GetXnatTransformd import GetXnatTransformd
from monai.transforms import LoadImaged, Compose
from torch.utils.data import DataLoader
from monai.data import CacheDataset


class TestXnatTransformd:

    def setup(self):
        self.test_data = [{'subject': 1, 'image': 'image1'},
                          {'subject': 2, 'image': 'image2'},
                          {'subject': 3, 'image': 'image3'}]

        self.xnat_configuration = {'server': 'http://localhost',
                                   'user': 'admin',
                                   'password': 'admin',
                                   'project': 'MLOPS_001'}

    def test_get_data(self):

        self.train_transforms = Compose(
            [
                GetXnatTransformd(keys=['subject'], xnat_configuration=self.xnat_configuration),
            ]
        )

        self.dataset = CacheDataset(data=self.test_data, transform=self.train_transforms)
        self.loader = DataLoader(self.dataset, batch_size=1,
                                 shuffle=True, num_workers=0)

        results = list(iter(self.loader))

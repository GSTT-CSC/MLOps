import configparser
import io
import logging
import os

import docker
import pytest
from mlflow.utils.git_utils import get_git_commit

from mlops.Experiment import Experiment

logger = logging.getLogger(__name__)


class TestExperiment:

    def setup_method(self):
        # currently only testing localhost code
        self.experiment = Experiment('test_entry.py', config_path='tests/data/test_config.cfg',
                                     project_path='tests/data')

    def test_check_dirty(self):
        """
        Test that the local and remote experiments are the same
        """
        # Need to set project_path at level of git directory for this test.
        self.experiment = Experiment('test_entry.py', 'tests/data/test_config.cfg', project_path='.')
        assert not self.experiment.check_dirty()

    def test_config_setup(self):
        self.experiment.config_setup()
        assert self.experiment.experiment_name == 'test_project'

    def test_env_setup(self):
        self.experiment.env_setup()
        assert os.getenv('MLFLOW_TRACKING_URI') == self.experiment.config['server']['MLFLOW_TRACKING_URI']

    def test_read_config(self):
        # Create config file and assert identical
        self.test_config = configparser.ConfigParser()
        self.test_config.read(self.experiment.config_path)
        assert self.experiment.config == self.test_config

    def test_init_experiment(self):
        self.experiment.init_experiment()
        assert self.experiment.experiment_id == '1'
        self.experiment.experiment_name = 'test_project_init_experiment'
        self.experiment.init_experiment()
        assert self.experiment.experiment_id == '2'

    def test_print_experiment_info(self, caplog):
        # Check correct information is printed to console
        with caplog.at_level(logging.INFO):
            self.experiment.print_experiment_info()  # Call function.
        assert 'Name: test_project' in caplog.text

    def test_build_project_file(self):
        if os.path.exists('MLproject'):
            os.remove('MLproject')
        self.experiment.build_project_file()
        assert os.path.exists(os.path.join(self.experiment.project_path, 'MLproject'))

    def test_build_experiment_image_subprocess(self):
        client = docker.from_env()
        self.experiment.build_experiment_image_subprocess(context_path='tests/data',
                                                          dockerfile_path=self.experiment.project_path + '/Dockerfile')
        images_list = [img['RepoTags'][0] for img in client.api.images() if img['RepoTags']]
        assert self.experiment.experiment_name + ':latest' in images_list

    def test_remove_run_image(self):
        client = docker.from_env()
        self.experiment.build_experiment_image_subprocess(context_path='tests/data',
                                                          dockerfile_path=self.experiment.project_path + '/Dockerfile')
        # tag the project image the same way mlflow tags its per-run image
        run_tag = get_git_commit(self.experiment.project_path)[:7]
        client.images.get(self.experiment.experiment_name + ':latest').tag(self.experiment.experiment_name, run_tag)

        self.experiment.remove_run_image(client)

        tags = [tag for img in client.images.list(name=self.experiment.experiment_name) for tag in img.tags]
        assert f'{self.experiment.experiment_name}:{run_tag}' not in tags
        assert self.experiment.experiment_name + ':latest' in tags

    def test_remove_replaced_image(self):
        client = docker.from_env()
        # separate image name so test_project:latest (used by test_run) is not replaced.
        # client.images.build(fileobj...) is the python version of docker build with the Dockerfile written inline. 
        name = 'mlops_test_replaced_image'
        old_image, _ = client.images.build(fileobj=io.BytesIO(b'FROM scratch\nLABEL build=old\n'), tag=name, rm=True)
        # rebuild that produces a different image, moving the tag and leaving old_image with no name
        new_image, _ = client.images.build(fileobj=io.BytesIO(b'FROM scratch\nLABEL build=new\n'), tag=name, rm=True)

        self.experiment.remove_replaced_image(client, old_image)
        with pytest.raises(docker.errors.ImageNotFound):
            client.images.get(old_image.id)

        # an image that still has its tag (cached or failed rebuild) is kept
        self.experiment.remove_replaced_image(client, new_image)
        assert client.images.get(name + ':latest').id == new_image.id

        client.images.remove(name + ':latest')

    def test_run(self, capsys):
        """
        this test will fail locally,  setup git in test data dir is done in github actions
        :param capsys:
        :return:
        """
        os.getcwd()
        self.experiment.build_project_file()
        self.experiment.run()
        captured = capsys.readouterr()
        assert 'succeeded' in captured.err

        # only the project image should remain, the mlflow per-run image is removed
        client = docker.from_env()
        tags = [tag for img in client.images.list(name=self.experiment.experiment_name) for tag in img.tags]
        assert tags == [self.experiment.experiment_name + ':latest']

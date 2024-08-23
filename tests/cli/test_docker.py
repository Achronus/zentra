import pytest
from unittest import mock
from unittest.mock import patch, MagicMock

from zentra_sdk.cli.builder.docker import DockerBuilder


class TestDockerBuilder:
    @pytest.fixture
    def mock_docker_client(self):
        with patch("docker.from_env") as mock_docker:
            yield mock_docker.return_value

    @pytest.fixture
    def docker_builder(self, mock_docker_client) -> DockerBuilder:
        return DockerBuilder(
            image_name="test_image",
            container_name="test_container",
            client=mock_docker_client,
        )

    @pytest.fixture
    def mock_open(self):
        with patch("builtins.open", mock.mock_open()) as mock_open:
            yield mock_open

    @pytest.fixture
    def mock_tarfile(self):
        with patch("tarfile.open", autospec=True) as mock_tarfile:
            mock_tarfile_instance = mock_tarfile.return_value
            mock_tarfile_instance.__enter__.return_value = mock_tarfile_instance
            mock_tarfile_instance.extractall = MagicMock()
            yield mock_tarfile_instance

    @pytest.fixture
    def mock_os_remove(self):
        with patch("os.remove") as mock_remove:
            yield mock_remove

    @staticmethod
    def test_pull(docker_builder: DockerBuilder, mock_docker_client):
        docker_builder.pull()
        mock_docker_client.images.pull.assert_called_once_with("test_image:latest")

    @staticmethod
    def test_run(docker_builder: DockerBuilder, mock_docker_client):
        mock_container = MagicMock()
        mock_docker_client.containers.run.return_value = mock_container
        container = docker_builder.run()

        assert container == mock_container
        mock_docker_client.containers.run.assert_called_once_with(
            "test_image:latest", name="test_container", detach=True
        )

    @staticmethod
    def test_copy(
        docker_builder: DockerBuilder, mock_open, mock_tarfile, mock_os_remove
    ):
        mock_container = MagicMock()
        mock_container.get_archive.return_value = (iter([b"data"]), None)

        docker_builder.copy(mock_container, "test_path")

        mock_open.assert_called_once_with("temp.tar", "wb")
        mock_os_remove.assert_called_once_with("temp.tar")

    @staticmethod
    def test_cleanup(docker_builder: DockerBuilder, mock_docker_client):
        mock_container = MagicMock()
        docker_builder.cleanup(mock_container)

        mock_container.stop.assert_called_once()
        mock_container.remove.assert_called_once()
        mock_docker_client.images.remove.assert_called_once_with("test_image")

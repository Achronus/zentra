import pytest
from unittest import mock
from unittest.mock import patch, MagicMock

import typer
from docker.errors import DockerException

from zentra_sdk.cli.commands.setup import Setup, SetupTasks
from zentra_sdk.cli.constants import SetupSuccessCodes


@pytest.fixture
def mock_docker():
    with patch("docker.from_env") as mock:
        yield mock


class TestSetup:
    @pytest.fixture
    def setup(self, tmp_path) -> Setup:
        return Setup(root=tmp_path)

    class TestProjectExists:
        @staticmethod
        def test_exists_with_files(setup: Setup):
            setup.paths.FRONTEND_PATH.mkdir()
            (setup.paths.FRONTEND_PATH / "test.txt").write_text("content")
            assert setup.project_exists()

        @staticmethod
        def test_exists_empty_directory(setup: Setup):
            setup.paths.FRONTEND_PATH.mkdir()
            setup.paths.BACKEND_PATH.mkdir()
            assert not setup.project_exists()

        @staticmethod
        def test_does_not_exist(setup: Setup):
            assert not setup.project_exists()

    class TestDockerInstalled:
        @staticmethod
        def test_true(mock_docker, setup: Setup):
            mock_client = MagicMock()
            mock_client.ping.return_value = True
            mock_docker.return_value = mock_client

            assert setup.docker_installed()

        @staticmethod
        def test_false(mock_docker, setup: Setup):
            mock_docker.side_effect = DockerException
            assert not setup.docker_installed()

        @staticmethod
        def test_raise(mock_docker, tmp_path):
            mock_docker.side_effect = DockerException
            with pytest.raises(typer.Exit):
                Setup(root=tmp_path)

    class TestBuild:
        @mock.patch.object(Setup, "project_exists", return_value=False)
        @mock.patch.object(
            SetupTasks,
            "get_tasks",
            return_value=[mock.Mock(), mock.Mock()],
        )
        def test_tasks_executed(
            self, mock_exists, mock_tasks: SetupTasks, setup: Setup
        ):
            with pytest.raises(typer.Exit):
                setup.build()

            for task in mock_tasks.get_tasks():
                task.assert_called_once()

        @mock.patch.object(Setup, "project_exists", return_value=False)
        @mock.patch.object(SetupTasks, "get_tasks", return_value=[])
        def test_completes(self, mock_exists, mock_tasks, setup: Setup):
            with pytest.raises(typer.Exit) as excinfo:
                setup.build()

            assert excinfo.value.exit_code == SetupSuccessCodes.COMPLETE

        @mock.patch.object(Setup, "project_exists", return_value=True)
        def test_project_exists(self, mock_exists, setup: Setup):
            with pytest.raises(typer.Exit) as excinfo:
                setup.build()

            assert excinfo.value.exit_code == SetupSuccessCodes.ALREADY_CONFIGURED


class TestSetupTasks:
    @pytest.fixture
    def setup_tasks(self) -> SetupTasks:
        return SetupTasks(test_logging=True)

    @pytest.fixture
    def mock_subprocess(self):
        with patch("subprocess.run") as mock_run:
            yield mock_run

    @staticmethod
    def test_build_backend(setup_tasks: SetupTasks, mock_subprocess: MagicMock):
        setup_tasks._build_backend()
        mock_subprocess.assert_called_once_with(
            ["zentra-api", "init", "backend", "--hide-output"]
        )

    def test_get_tasks(self, setup_tasks: SetupTasks):
        tasks = setup_tasks.get_tasks()

        target = [
            setup_tasks._build_backend,
            setup_tasks._build_frontend,
        ]
        assert tasks == target
        assert len(tasks) == len(target)

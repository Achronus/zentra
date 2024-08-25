import pytest
from unittest import mock
from unittest.mock import patch, MagicMock

import typer
from docker.errors import DockerException

from zentra_sdk.cli.commands.setup import Setup, SetupTasks
from zentra_sdk.cli.constants import (
    FRONTEND_FILES_TO_REMOVE,
    ProjectPaths,
    SetupSuccessCodes,
)


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
    def setup_tasks(self, tmp_path) -> SetupTasks:
        return SetupTasks(paths=ProjectPaths(tmp_path), test_logging=True)

    @pytest.fixture
    def mock_subprocess(self):
        with patch("subprocess.run") as mock_run:
            yield mock_run

    @pytest.fixture
    def mock_os_remove(self):
        with patch("os.remove") as mock_remove:
            yield mock_remove

    @pytest.fixture
    def mock_shutil_copytree(self):
        with patch("shutil.copytree") as mock_copytree:
            yield mock_copytree

    @pytest.fixture
    def mock_os_rename(self):
        with patch("os.rename") as mock_rename:
            yield mock_rename

    @staticmethod
    def test_build_backend(setup_tasks: SetupTasks, mock_subprocess: MagicMock):
        setup_tasks._build_backend()
        mock_subprocess.assert_called_once_with(
            ["zentra-api", "init", "backend", "--hide-output"]
        )

    @staticmethod
    def test_remove_files(setup_tasks: SetupTasks, mock_os_remove: MagicMock):
        files_to_remove = FRONTEND_FILES_TO_REMOVE
        setup_tasks.paths.FRONTEND_PATH.mkdir(parents=True, exist_ok=True)
        for file_name in files_to_remove:
            (setup_tasks.paths.FRONTEND_PATH / file_name).touch()

        setup_tasks._remove_files()

        for file_name in files_to_remove:
            mock_os_remove.assert_any_call(setup_tasks.paths.FRONTEND_PATH / file_name)

        assert mock_os_remove.call_count == len(files_to_remove)

    @staticmethod
    def test_move_files(
        setup_tasks: SetupTasks,
        mock_shutil_copytree: MagicMock,
        mock_os_rename: MagicMock,
    ):
        (setup_tasks.package_paths.FRONTEND).mkdir(parents=True, exist_ok=True)
        (setup_tasks.package_paths.ROOT).mkdir(parents=True, exist_ok=True)

        (setup_tasks.paths.FRONTEND_PATH).mkdir(parents=True, exist_ok=True)
        (setup_tasks.paths.ROOT).mkdir(parents=True, exist_ok=True)

        env_local_template = setup_tasks.paths.FRONTEND_PATH / ".env.local.template"
        env_local_template.touch()

        setup_tasks._move_files()

        mock_shutil_copytree.assert_any_call(
            setup_tasks.package_paths.FRONTEND,
            setup_tasks.paths.FRONTEND_PATH,
            dirs_exist_ok=True,
        )
        mock_shutil_copytree.assert_any_call(
            setup_tasks.package_paths.ROOT, setup_tasks.paths.ROOT, dirs_exist_ok=True
        )
        mock_os_rename.assert_called_once_with(
            env_local_template, setup_tasks.paths.ENV_LOCAL
        )

    @staticmethod
    def test_get_tasks(setup_tasks: SetupTasks):
        tasks = setup_tasks.get_tasks()

        target = [
            setup_tasks._build_backend,
            setup_tasks._build_frontend,
            setup_tasks._remove_files,
            setup_tasks._move_files,
        ]
        assert tasks == target
        assert len(tasks) == len(target)

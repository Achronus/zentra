import os
from unittest.mock import MagicMock, patch
import pytest
import typer

from cli.conf.constants import (
    CommonErrorCodes,
    GenerateErrorCodes,
    GenerateSuccessCodes,
    LocalUploadthingFilepaths,
)
from cli.conf.format import name_from_camel_case
from cli.conf.storage import ConfigExistStorage, PathStorage, SetupPathStorage
from cli.tasks.controllers.base import status, BaseController
from cli.tasks.controllers.setup import SetupController
from cli.tasks.controllers.generate import GenerateController
from cli.tasks.generate import Generate

from zentra.core import Page, Zentra
from zentra.ui import FileUpload, Form, FormField
from zentra.ui.control import Button, Input
from zentra.ui.notification import AlertDialog
from zentra.ui.presentation import Card


class TestStatus:
    def test_success(self):
        @status
        def success_task():
            pass

        result, e = success_task()
        assert result is True and e is None

    def test_fail(self):
        @status
        def failing_task():
            raise Exception("Test exception in 'test_controller.py' -> 'TestStatus'")

        result, e = failing_task()
        assert result is False, e is ValueError


class TestBaseController:
    def test_run(self):
        @status
        @staticmethod
        def task():
            pass

        @status
        @staticmethod
        def task_fail():
            raise Exception(
                "Test exception in 'test_controller.py' -> 'TestBaseController'"
            )

        tasks = [(task, "Task 1"), (task_fail, "Task 2")]
        controller = BaseController(tasks=tasks)
        with pytest.raises(Exception):
            controller.run()
            assert all(
                [
                    len(controller.called_tasks) == 2,
                    controller.called_tasks[0] == ("1. Task 1...", True),
                    controller.called_tasks[1] == ("2. Task 2...", False),
                ]
            ), controller.called_tasks


class TestSetupController:
    @pytest.fixture
    def controller(self, tmp_path) -> SetupController:
        return SetupController(
            SetupPathStorage(
                config=os.path.join(tmp_path, "zentra_init.py"),
                models=os.path.join(tmp_path, "zentra_models"),
                demo=os.path.join(tmp_path, "zentra_models_demo"),
                zentra_local=os.path.join(tmp_path, "zentra_local"),
                local_demo=os.path.join(tmp_path, "zentra_local_demo"),
            ),
            config_storage=ConfigExistStorage(),
        )

    @staticmethod
    def test_make_models_dir_true(controller: SetupController):
        controller.config_storage.models_folder_exists = True
        controller._make_models_dir()

        assert not os.path.exists(controller.paths.models)

    @staticmethod
    def test_make_models_dir_false(controller: SetupController):
        controller.config_storage.models_folder_exists = False
        controller._make_models_dir()

        assert os.path.exists(controller.paths.models)

    @staticmethod
    def test_make_config_file_true(controller: SetupController):
        controller.config_storage.config_file_exists = True
        controller._make_config_file()

        assert not os.path.exists(controller.paths.config)

    @staticmethod
    def test_make_config_file_false(controller: SetupController):
        local_config_filepath = os.path.join(
            controller.paths.zentra_local, controller.paths.config
        )
        new_config_filepath = os.path.join(
            controller.paths.models, controller.paths.config
        )

        os.makedirs(controller.paths.zentra_local, exist_ok=True)
        os.makedirs(controller.paths.models, exist_ok=True)

        with open(local_config_filepath, "w") as f:
            f.write("test")

        controller.config_storage.config_file_exists = False
        controller._make_config_file()

        assert os.path.exists(new_config_filepath)

    @staticmethod
    def test_create_missing_files(controller: SetupController):
        try:
            controller.create_missing_files()
        except typer.Exit:
            assert False

    @staticmethod
    def test_create_demo_files(controller: SetupController):
        test_file = os.path.join(controller.paths.local_demo, "file1.txt")
        new_test_filepath = os.path.join(controller.paths.demo, test_file)

        os.makedirs(controller.paths.local_demo, exist_ok=True)

        with open(test_file, "w") as f:
            f.write("test")

        controller.config_storage.config_file_exists = False
        controller.create_demo_files()

        checks = [
            os.path.exists(controller.paths.demo),
            os.path.exists(new_test_filepath),
        ]
        assert all(checks)


class TestModelStorage:
    def test_nextjs_project_false(self):
        nextjs_project = False

        result = (
            LocalUploadthingFilepaths.BASE_NEXTJS
            if nextjs_project
            else LocalUploadthingFilepaths.BASE_BASIC
        )
        assert result == LocalUploadthingFilepaths.BASE_BASIC

    def test_nextjs_project_true(self):
        nextjs_project = True

        result = (
            LocalUploadthingFilepaths.BASE_NEXTJS
            if nextjs_project
            else LocalUploadthingFilepaths.BASE_BASIC
        )
        assert result == LocalUploadthingFilepaths.BASE_NEXTJS


class TestGenerate:
    @pytest.fixture
    def path_storage(self, tmp_path) -> PathStorage:
        return PathStorage(
            config=os.path.join(tmp_path, "test_models", "config_init.py"),
            models=os.path.join(tmp_path, "test_models"),
            generated_zentra=os.path.join(tmp_path, "zentra_generated"),
            local_ui_base=os.path.join(tmp_path, "test_ui_base"),
            generated_ui_base=os.path.join(tmp_path, "test_generated_base"),
        )

    @pytest.fixture
    def generate(self, path_storage: PathStorage) -> Generate:
        return Generate(paths=path_storage)

    class TestCheckConfig:
        @staticmethod
        def test_model_folder_exists_error(generate: Generate):
            with pytest.raises(typer.Exit) as e:
                generate.init_checks()

            assert e.value.exit_code == CommonErrorCodes.MODELS_DIR_MISSING

        @staticmethod
        def test_config_file_exists_error(generate: Generate):
            os.makedirs(generate.paths.models)
            with pytest.raises(typer.Exit) as e:
                generate.init_checks()

            assert e.value.exit_code == CommonErrorCodes.CONFIG_MISSING

        @staticmethod
        def test_config_file_empty(generate: Generate):
            os.makedirs(generate.paths.models)
            with open(generate.paths.config, "w") as f:
                f.write("")

            with pytest.raises(typer.Exit) as e:
                generate.init_checks()

            assert e.value.exit_code == CommonErrorCodes.CONFIG_EMPTY

        @staticmethod
        def test_config_file_valid_error(generate: Generate):
            os.makedirs(generate.paths.models)
            with open(generate.paths.config, "w") as f:
                f.write("from zentra.core import Zentra\nzentra = Zentra()")

            with pytest.raises(typer.Exit) as e:
                generate.check_config_valid()

            assert e.value.exit_code == CommonErrorCodes.INVALID_CONFIG

        @staticmethod
        def test_check_config_valid_success(generate: Generate):
            os.makedirs(generate.paths.models, exist_ok=True)
            with open(generate.paths.config, "w") as f:
                f.write(
                    "from zentra.core import Zentra\nzentra = Zentra()\nzentra.register()"
                )

            assert generate.check_config_valid() is None

    class TestCheckComponentsExist:
        @staticmethod
        def test_no_new_components_raise(generate: Generate):
            os.makedirs(generate.paths.generated_zentra)

            with open(
                os.path.join(generate.paths.generated_zentra, "file1.txt"), "w"
            ) as f:
                f.write("test")

            with pytest.raises(typer.Exit) as e:
                generate.check_components_exist()

            assert e.value.exit_code == GenerateSuccessCodes.NO_NEW_COMPONENTS

        @staticmethod
        def test_no_raise(generate: Generate):
            assert generate.check_components_exist() is None

    class TestCreateComponents:
        @staticmethod
        def test_no_components_error(generate: Generate):
            os.makedirs(generate.paths.models, exist_ok=True)
            with open(generate.paths.config, "w") as f:
                f.write(
                    "from zentra.core import Zentra\nzentra = Zentra()\n\nzentra.register([])"
                )

            mock_zentra_module = MagicMock()
            setattr(mock_zentra_module, "zentra", Zentra())

            with patch("importlib.import_module", return_value=mock_zentra_module):
                with pytest.raises(typer.Exit) as e:
                    generate.create_components()

            assert e.value.exit_code == GenerateErrorCodes.NO_COMPONENTS

        @staticmethod
        def test_create_components_success(generate: Generate):
            os.makedirs(generate.paths.models, exist_ok=True)
            os.makedirs(generate.paths.local_ui_base, exist_ok=True)
            with open(generate.paths.config, "w") as f:
                f.write(
                    "from zentra.core import Zentra\nfrom zentra.ui.control import Button\n\nzentra = Zentra()\n\nzentra.register([])"
                )

            mock_zentra_module = MagicMock()
            setattr(mock_zentra_module, "zentra", Zentra())
            mock_zentra_module.zentra.register(
                [Button(name="userBtn", text="Click me!", variant="primary")]
            )

            with patch("importlib.import_module", return_value=mock_zentra_module):
                generate.create_components()


class TestGenerateController:
    @pytest.fixture
    def path_storage(self, tmp_path) -> PathStorage:
        return PathStorage(
            config=os.path.join(tmp_path, "test_models", "config_init.py"),
            models=os.path.join(tmp_path, "test_models"),
            generated_zentra=os.path.join(tmp_path, "zentra_generated"),
            local_ui_base=os.path.join(tmp_path, "test_ui_base"),
            generated_ui_base=os.path.join(tmp_path, "test_generated_base"),
        )

    @pytest.fixture
    def page(self) -> Page:
        return Page(
            name="AgencyDetails",
            components=[
                AlertDialog(
                    name="agencyAlertDialog",
                    content=[
                        Card(
                            name="agencyInfo",
                            title="Agency Information",
                            description="Let's create an agency for your business. You can edit agency settings later from the agency settings tab.",
                            content=[
                                Form(
                                    name="agencyForm",
                                    fields=[
                                        FormField(
                                            name="agencyLogo",
                                            label="Agency Logo",
                                            content=FileUpload(name="agencyLogo"),
                                        ),
                                        FormField(
                                            name="name",
                                            label="Agency Name",
                                            content=Input(
                                                name="name",
                                                label="Agency Name",
                                                placeholder="Your Agency Name",
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    @pytest.fixture
    def zentra(self, page: Page) -> Zentra:
        zentra = Zentra()
        zentra.register([page])
        return zentra

    @pytest.fixture
    def controller(
        self, path_storage: PathStorage, zentra: Zentra
    ) -> GenerateController:
        return GenerateController(zentra, paths=path_storage)

    class TestExtractModels:
        @pytest.fixture
        def names(self, zentra: Zentra) -> list[str]:
            return [
                f"{name_from_camel_case(name)}.tsx" for name in zentra.component_names
            ]

        def test_formatted_names(self, names: list[str]):
            valid_names = [
                "alert-dialog.tsx",
                "form.tsx",
                "card.tsx",
                "file-upload.tsx",
                "input.tsx",
            ]

            assert len(names) == len(valid_names)

        def test_ut_to_generate(self, controller: GenerateController):
            controller.extract_models()
            result = controller.storage.UT_TO_GENERATE
            valid = ["file-upload.tsx"]
            assert len(result) == len(valid)

        def test_ui_to_generate(self, controller: GenerateController):
            controller.extract_models()
            result = controller.storage.UI_TO_GENERATE
            valid = [
                "alert-dialog.tsx",
                "form.tsx",
                "card.tsx",
                "input.tsx",
            ]
            assert len(result) == len(valid)

    class TestCreateFiles:
        @staticmethod
        def test_src_error(controller: GenerateController):
            with pytest.raises(typer.Exit) as e_info:
                controller._copy_base_ui()

            assert e_info.value.exit_code == CommonErrorCodes.SRC_DIR_MISSING

        @staticmethod
        def test_dest_error(controller: GenerateController):
            os.mkdir(controller.paths.local_ui_base)
            with pytest.raises(typer.Exit) as e_info:
                controller._copy_base_ui()

            assert e_info.value.exit_code == GenerateErrorCodes.GENERATE_DIR_MISSING

        @staticmethod
        def create_files_valid(setup_dirs, controller: GenerateController):
            src, dest = setup_dirs

            open(os.path.join(src, "file1.txt"), "w").close()
            open(os.path.join(src, "file2.txt"), "w").close()

            controller.create_files()

            checks = [
                os.path.exists(os.path.join(dest, "file1.txt")),
                os.path.exists(os.path.join(dest, "file2.txt")),
            ]

            assert all(checks)

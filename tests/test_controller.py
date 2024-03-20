import os
from unittest.mock import MagicMock, patch
import pytest
import typer

from cli.conf.constants import (
    CommonErrorCodes,
    GenerateErrorCodes,
    GenerateSuccessCodes,
)
from cli.conf.format import name_from_camel_case
from cli.conf.storage import (
    ConfigExistStorage,
    GeneratePathStorage,
    SetupPathStorage,
)
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
                config=os.path.join(tmp_path, "zentra_models", "zentra_init.py"),
                models=os.path.join(tmp_path, "zentra_models"),
                local=os.path.join(tmp_path, "zentra_config"),
                demo=os.path.join(tmp_path, "zentra_config", "_demo"),
                local_config=os.path.join(tmp_path, "zentra_config", "zentra_init.py"),
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
        os.makedirs(controller.paths.local, exist_ok=True)
        os.makedirs(controller.paths.models, exist_ok=True)

        with open(controller.paths.local_config, "w") as f:
            f.write("test")

        controller.config_storage.config_file_exists = False
        controller._make_config_file()

        assert os.path.exists(controller.paths.config)

    @staticmethod
    def test_create_missing_files(controller: SetupController):
        try:
            controller.create_missing_files()
        except typer.Exit:
            assert False

    @staticmethod
    def test_create_demo_files(controller: SetupController):
        test_file = os.path.join(controller.paths.demo, "file1.txt")
        new_test_filepath = os.path.join(controller.paths.demo, test_file)

        os.makedirs(controller.paths.demo, exist_ok=True)

        with open(test_file, "w") as f:
            f.write("test")

        controller.config_storage.config_file_exists = False
        controller.create_demo_files()

        checks = [
            os.path.exists(controller.paths.demo),
            os.path.exists(new_test_filepath),
        ]
        assert all(checks)


class TestGenerate:
    @pytest.fixture
    def path_storage(self, tmp_path) -> GeneratePathStorage:
        return GeneratePathStorage(
            config=os.path.join(tmp_path, "test_models", "config_init.py"),
            models=os.path.join(tmp_path, "test_models"),
            component=os.path.join(tmp_path, "test_component"),
            generate=os.path.join(tmp_path, "zentra_generated"),
        )

    @pytest.fixture
    def generate(self, path_storage: GeneratePathStorage) -> Generate:
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
        def test_success(generate: Generate):
            os.makedirs(generate.paths.models, exist_ok=True)
            with open(generate.paths.config, "w") as f:
                f.write(
                    "from zentra.core import Zentra\nfrom zentra.ui.control import Button\n\nzentra = Zentra()\n\nzentra.register([])"
                )

            btn_dir_path = os.path.join(generate.paths.component, "ui", "base")
            btn_path = os.path.join(btn_dir_path, "button.tsx")

            os.makedirs(btn_dir_path)
            with open(btn_path, "w") as f:
                f.write("test")

            mock_zentra_module = MagicMock()
            setattr(mock_zentra_module, "zentra", Zentra())
            mock_zentra_module.zentra.register(
                [Button(name="userBtn", text="Click me!", variant="primary")]
            )

            with patch("importlib.import_module", return_value=mock_zentra_module):
                with pytest.raises(typer.Exit) as e:
                    generate.create_components()

            assert e.value.exit_code == GenerateSuccessCodes.COMPLETE


class TestGenerateController:
    @pytest.fixture
    def path_storage(self, tmp_path) -> GeneratePathStorage:
        return GeneratePathStorage(
            config=os.path.join(tmp_path, "test_models", "config_init.py"),
            models=os.path.join(tmp_path, "test_models"),
            component=os.path.join(tmp_path, "test_local"),
            generate=os.path.join(tmp_path, "test_generated"),
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
                                    layout=[2],
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
        self, path_storage: GeneratePathStorage, zentra: Zentra
    ) -> GenerateController:
        return GenerateController(zentra, paths=path_storage)

    @pytest.fixture
    def setup_example_models(
        self, controller: GenerateController
    ) -> tuple[str, str, str]:
        src1 = os.path.join(controller.paths.component, "uploadthing", "base")
        src2 = os.path.join(controller.paths.component, "ui", "base")
        dest = os.path.join(controller.paths.generate)

        os.makedirs(src1, exist_ok=True)
        os.makedirs(src2, exist_ok=True)
        os.makedirs(dest, exist_ok=True)

        controller.extract_models()
        for folder, file in controller.storage.components.generate:
            if folder == "uploadthing":
                with open(os.path.join(src1, file), "w") as f:
                    f.write("test")
            elif folder == "ui":
                with open(os.path.join(src2, file), "w") as f:
                    f.write("test")

        return src1, src2, dest

    @pytest.fixture
    def example_existing_models(self, controller: GenerateController) -> None:
        controller.storage.components.existing = [
            ("uploadthing", "uploadthing.ts"),
            ("uploadthing", "core.ts"),
            ("uploadthing", "route.ts"),
        ]

    @pytest.fixture
    def example_models_to_remove(self, controller: GenerateController) -> None:
        controller.storage.components.remove = [
            ("uploadthing", "uploadthing.ts"),
            ("uploadthing", "core.ts"),
            ("uploadthing", "route.ts"),
        ]

    @pytest.fixture
    def example_models_to_generate(self, controller: GenerateController) -> None:
        controller.storage.components.generate = [
            ("uploadthing", "uploadthing.ts"),
            ("uploadthing", "core.ts"),
            ("uploadthing", "route.ts"),
        ]

    class TestGetAndFormatModels:
        @pytest.fixture
        def names(self, zentra: Zentra) -> list[str]:
            return [
                f"{name_from_camel_case(name)}.tsx" for name in zentra.names.components
            ]

        def test_formatted_names(self, controller: GenerateController):
            valid_names = [
                "alert-dialog.tsx",
                "form.tsx",
                "card.tsx",
                "file-upload.tsx",
                "input.tsx",
            ]

            result = controller._get_and_format_models(
                controller.storage.base_names.components
            )
            assert len(result) == len(valid_names)

        def test_files_to_generate(self, controller: GenerateController):
            controller.extract_models()
            result = controller.storage.components.generate
            valid = [
                ("ui", "alert-dialog.tsx"),
                ("ui", "card.tsx"),
                ("ui", "form.tsx"),
                ("ui", "input.tsx"),
                ("uploadthing", "core.ts"),
                ("uploadthing", "route.ts"),
                ("uploadthing", "uploadthing.ts"),
            ]
            assert len(result) == len(valid)

        def test_folders_to_generate(self, controller: GenerateController):
            controller.extract_models()
            result = controller.storage.folders_to_generate
            valid = ["ui", "uploadthing"]
            assert len(result) == len(valid)

    class TestUpdateFiles:
        @staticmethod
        def test_generate_succes(setup_example_models, controller: GenerateController):
            _, _, dest = setup_example_models
            dest = os.path.join(dest, "uploadthing")

            controller.update_files()

            checks = [
                os.path.exists(os.path.join(dest, "uploadthing.ts")),
                os.path.exists(os.path.join(dest, "core.ts")),
                os.path.exists(os.path.join(dest, "route.ts")),
            ]

            assert all(checks), controller.storage.components.generate

        @staticmethod
        def test_removal_success(setup_example_models, controller: GenerateController):
            _, _, dest = setup_example_models
            dest = os.path.join(dest, "uploadthing")

            files_to_remove = [
                ("uploadthing", "uploadthing.ts"),
                ("uploadthing", "core.ts"),
                ("uploadthing", "route.ts"),
            ]

            controller.storage.components.remove = files_to_remove
            controller.storage.components.counts.remove = len(files_to_remove)

            controller.update_files()

            assert not os.path.exists(dest), controller.storage.components.counts.remove

    class TestCheckForNewComponents:
        @staticmethod
        def test_valid_raise(
            example_models_to_generate,
            example_existing_models,
            controller: GenerateController,
        ):
            with pytest.raises(typer.Exit) as e:
                controller._check_for_new_components(
                    controller.storage.components.existing,
                    controller.storage.components.generate,
                )

            assert e.value.exit_code == GenerateSuccessCodes.NO_NEW_COMPONENTS

    class TestGetModelChanges:
        @staticmethod
        def test_valid_lists(controller: GenerateController):
            existing_models = [
                ("ui", "alert-dialog.tsx"),
                ("ui", "button.tsx"),
                ("ui", "card.tsx"),
                ("ui", "form.tsx"),
                ("ui", "input.tsx"),
                ("uploadthing", "core.ts"),
                ("uploadthing", "route.ts"),
                ("uploadthing", "uploadthing.ts"),
            ]
            controller.storage.components.existing = existing_models

            generate_list = [
                ("ui", "alert-dialog.tsx"),
                ("ui", "button.tsx"),
                ("ui", "card.tsx"),
                ("ui", "form.tsx"),
                ("ui", "input.tsx"),
            ]

            model_updates = controller._get_model_updates(
                existing_models, generate_list
            )
            to_remove, to_add = controller._get_model_changes(model_updates)

            checks = [
                len(to_remove) == 3,
                len(to_add) == 0,
            ]

            assert all(checks), model_updates

    class TestStoreComponents:
        @staticmethod
        def test_valid_counts(controller: GenerateController):
            existing_models = [
                ("ui", "alert-dialog.tsx"),
                ("ui", "button.tsx"),
                ("ui", "card.tsx"),
                ("ui", "form.tsx"),
                ("ui", "input.tsx"),
                ("uploadthing", "core.ts"),
                ("uploadthing", "route.ts"),
                ("uploadthing", "uploadthing.ts"),
            ]
            controller.storage.components.existing = existing_models

            generate_list = [
                ("ui", "alert-dialog.tsx"),
                ("ui", "button.tsx"),
                ("ui", "card.tsx"),
                ("ui", "form.tsx"),
                ("ui", "input.tsx"),
                ("ui", "accordion.tsx"),
                ("ui", "tooltip.tsx"),
            ]

            model_updates = controller._get_model_updates(
                existing_models, generate_list
            )
            controller._store_components(model_updates)

            checks = [
                controller.storage.components.counts.generate == 2,
                controller.storage.components.counts.remove == 1,
            ]

            assert all(checks), model_updates

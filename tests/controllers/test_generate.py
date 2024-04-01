import pytest
import os
from unittest.mock import MagicMock, patch
import typer

from cli.conf.constants import (
    CommonErrorCodes,
    GenerateErrorCodes,
    GenerateSuccessCodes,
)
from cli.conf.format import name_from_camel_case
from cli.conf.storage import GeneratePathStorage
from cli.tasks.controllers.generate import GenerateController
from cli.tasks.generate import Generate

from zentra.core import Page, Zentra
from zentra.ui import Form, FormField
from zentra.ui.control import Button, Input
from zentra.ui.notification import AlertDialog
from zentra.ui.presentation import Card
from zentra.uploadthing import FileUpload


@pytest.fixture
def path_storage(tmp_path) -> GeneratePathStorage:
    return GeneratePathStorage(
        config=os.path.join(tmp_path, "test_models", "config_init.py"),
        models=os.path.join(tmp_path, "test_models"),
        component=os.path.join(tmp_path, "test_local"),
        generate=os.path.join(tmp_path, "test_generated"),
        templates=os.path.join(tmp_path, "zentra_templates"),
    )


@pytest.fixture
def generate(path_storage: GeneratePathStorage) -> Generate:
    return Generate(paths=path_storage)


@pytest.fixture
def generate_controller(
    path_storage: GeneratePathStorage, zentra: Zentra
) -> GenerateController:
    return GenerateController(zentra, paths=path_storage)


@pytest.fixture
def page() -> Page:
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
                                        content=FileUpload(),
                                    ),
                                    FormField(
                                        name="name",
                                        label="Agency Name",
                                        content=Input(
                                            id="agencyName",
                                            type="text",
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
def zentra(page: Page) -> Zentra:
    zentra = Zentra()
    zentra.register([page])
    return zentra


class TestGenerate:
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
                [Page(name="ButtonPage", components=[Button(text="Click me!")])]
            )

            with patch("importlib.import_module", return_value=mock_zentra_module):
                with pytest.raises(typer.Exit) as e:
                    generate.create_components()

            assert e.value.exit_code == GenerateSuccessCodes.COMPLETE


class TestGenerateController:
    @pytest.fixture
    def setup_example_models(
        self, generate_controller: GenerateController
    ) -> tuple[str, str, str]:
        src1 = os.path.join(generate_controller.paths.component, "uploadthing", "base")
        src2 = os.path.join(generate_controller.paths.component, "ui", "base")
        dest = os.path.join(generate_controller.paths.generate)

        os.makedirs(src1, exist_ok=True)
        os.makedirs(src2, exist_ok=True)
        os.makedirs(dest, exist_ok=True)

        generate_controller.extract_models()
        for folder, file in generate_controller.storage.components.generate:
            if folder == "uploadthing":
                with open(os.path.join(src1, file), "w") as f:
                    f.write("test")
            elif folder == "ui":
                with open(os.path.join(src2, file), "w") as f:
                    f.write("test")

        return src1, src2, dest

    @pytest.fixture
    def example_existing_models(self, generate_controller: GenerateController) -> None:
        generate_controller.storage.components.existing = [
            ("uploadthing", "uploadthing.ts"),
            ("uploadthing", "core.ts"),
            ("uploadthing", "route.ts"),
        ]

    @pytest.fixture
    def example_models_to_remove(self, generate_controller: GenerateController) -> None:
        generate_controller.storage.components.remove = [
            ("uploadthing", "uploadthing.ts"),
            ("uploadthing", "core.ts"),
            ("uploadthing", "route.ts"),
        ]

    @pytest.fixture
    def example_models_to_generate(
        self, generate_controller: GenerateController
    ) -> None:
        generate_controller.storage.components.generate = [
            ("uploadthing", "uploadthing.ts"),
            ("uploadthing", "core.ts"),
            ("uploadthing", "route.ts"),
        ]

    class TestGetAndFormatModels:
        @pytest.fixture
        def names(self, zentra: Zentra) -> list[str]:
            return [
                f"{name_from_camel_case(name)}.tsx"
                for name in zentra.name_storage.components
            ]

        def test_formatted_names(self, generate_controller: GenerateController):
            valid_names = [
                "alert-dialog.tsx",
                "card.tsx",
                "file-upload.tsx",
                "form.tsx",
                "input.tsx",
            ]

            result = generate_controller._get_and_format_models(
                generate_controller.storage.base_names.components
            )
            assert len(result) == len(valid_names), result

        def test_files_to_generate(self, generate_controller: GenerateController):
            generate_controller.extract_models()
            result = generate_controller.storage.components.generate
            valid = [
                ("ui", "alert-dialog.tsx"),
                ("ui", "card.tsx"),
                ("ui", "form.tsx"),
                ("ui", "input.tsx"),
                ("uploadthing", "file-upload.tsx"),
            ]
            assert len(result) == len(valid)

        def test_folders_to_generate(self, generate_controller: GenerateController):
            generate_controller.extract_models()
            result = generate_controller.storage.folders_to_generate
            valid = ["ui", "uploadthing"]
            assert len(result) == len(valid)

    class TestUpdateFiles:
        @staticmethod
        def test_generate_success(
            setup_example_models, generate_controller: GenerateController
        ):
            _, _, dest = setup_example_models
            dest = os.path.join(dest, "uploadthing")

            generate_controller.update_files()

            checks = [
                os.path.exists(os.path.join(dest, "file-upload.tsx")),
            ]

            assert all(checks), checks

        @staticmethod
        def test_removal_success(
            setup_example_models, generate_controller: GenerateController
        ):
            _, _, dest = setup_example_models
            dest = os.path.join(dest, "uploadthing")

            files_to_remove = [
                ("uploadthing", "file_upload.tsx"),
            ]

            generate_controller.storage.components.remove = files_to_remove
            generate_controller.storage.components.counts.remove = len(files_to_remove)

            generate_controller.update_files()

            assert not os.path.exists(dest), os.path.exists(dest)

    class TestCheckForNewComponents:
        @staticmethod
        def test_valid_raise(
            example_models_to_generate,
            example_existing_models,
            generate_controller: GenerateController,
        ):
            with pytest.raises(typer.Exit) as e:
                generate_controller._check_for_new_components(
                    generate_controller.storage.components.existing,
                    generate_controller.storage.components.generate,
                )

            assert e.value.exit_code == GenerateSuccessCodes.NO_NEW_COMPONENTS

    class TestGetModelChanges:
        @staticmethod
        def test_valid_lists(generate_controller: GenerateController):
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
            generate_controller.storage.components.existing = existing_models

            generate_list = [
                ("ui", "alert-dialog.tsx"),
                ("ui", "button.tsx"),
                ("ui", "card.tsx"),
                ("ui", "form.tsx"),
                ("ui", "input.tsx"),
            ]

            model_updates = generate_controller._get_model_updates(
                existing_models, generate_list
            )
            to_remove, to_add = generate_controller._get_model_changes(model_updates)

            checks = [
                len(to_remove) == 3,
                len(to_add) == 0,
            ]

            assert all(checks), model_updates

    class TestStoreComponents:
        @staticmethod
        def test_valid_counts(generate_controller: GenerateController):
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
            generate_controller.storage.components.existing = existing_models

            generate_list = [
                ("ui", "alert-dialog.tsx"),
                ("ui", "button.tsx"),
                ("ui", "card.tsx"),
                ("ui", "form.tsx"),
                ("ui", "input.tsx"),
                ("ui", "accordion.tsx"),
                ("ui", "tooltip.tsx"),
            ]

            model_updates = generate_controller._get_model_updates(
                existing_models, generate_list
            )
            generate_controller._store_components(model_updates)

            checks = [
                generate_controller.storage.components.counts.generate == 2,
                generate_controller.storage.components.counts.remove == 1,
            ]

            assert all(checks), model_updates

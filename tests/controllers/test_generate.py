import pytest
import os
from unittest.mock import MagicMock, patch
import typer

from cli.conf.constants import (
    GITHUB_COMPONENTS_DIR,
    CommonErrorCodes,
    GenerateErrorCodes,
    GenerateSuccessCodes,
)
from cli.conf.format import name_from_camel_case
from cli.conf.storage import CountStorage, GeneratePathStorage, ModelFileStorage
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
        components=os.path.join(tmp_path, "test_generated"),
        templates=os.path.join(tmp_path, "zentra_templates"),
        lib=os.path.join(tmp_path, "zentra_lib"),
    )


@pytest.fixture
def generate(path_storage: GeneratePathStorage) -> Generate:
    return Generate(paths=path_storage)


@pytest.fixture
def generate_controller(
    path_storage: GeneratePathStorage, zentra: Zentra
) -> GenerateController:
    return GenerateController(
        url=GITHUB_COMPONENTS_DIR, zentra=zentra, paths=path_storage
    )


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
    def example_existing_user_models(self) -> tuple[list, list]:
        existing_models = [
            ("ui", "input.tsx"),
            ("ui", "form.tsx"),
            ("uploadthing", "file-upload.tsx"),
        ]
        user_models = [
            ("uploadthing", "file-upload.tsx"),
            ("ui", "card.tsx"),
        ]
        return existing_models, user_models

    class TestDetectModels:
        @pytest.fixture
        def names(self, zentra: Zentra) -> list[str]:
            return [
                f"{name_from_camel_case(name)}.tsx"
                for name in zentra.name_storage.components
            ]

        def test_user_models(self, generate_controller: GenerateController):
            valid = [
                ("ui", "alert-dialog.tsx"),
                ("ui", "card.tsx"),
                ("ui", "form.tsx"),
                ("ui", "input.tsx"),
                ("uploadthing", "file-upload.tsx"),
            ]
            result = generate_controller.local_extractor.user_models()
            assert result == valid, result

        def test_existing_models(self, generate_controller: GenerateController):
            dest_dir = os.path.join(generate_controller.paths.components, "ui")
            file1 = os.path.join(dest_dir, "accordion.tsx")
            os.makedirs(dest_dir)

            with open(file1, "w") as f:
                f.write("test")

            valid = [("ui", "accordion.tsx")]
            result = generate_controller.local_extractor.existing_models()
            assert result == valid, result

        def test_files_to_generate(self, generate_controller: GenerateController):
            generate_controller.detect_models()
            result = generate_controller.storage.components.generate
            valid = [
                ("ui", "alert-dialog.tsx"),
                ("ui", "card.tsx"),
                ("ui", "form.tsx"),
                ("ui", "input.tsx"),
                ("uploadthing", "file-upload.tsx"),
            ]
            assert len(result) == len(valid)

        def test_no_new_components_error(self, generate_controller: GenerateController):
            user_models = [
                ("ui", "alert-dialog.tsx"),
                ("ui", "card.tsx"),
                ("ui", "form.tsx"),
            ]
            existing_models = [
                ("ui", "alert-dialog.tsx"),
                ("ui", "card.tsx"),
                ("ui", "form.tsx"),
            ]
            with pytest.raises(typer.Exit) as e:
                generate_controller.local_extractor.no_new_components_check(
                    user_models, existing_models
                )

            assert e.value.exit_code == GenerateSuccessCodes.NO_NEW_COMPONENTS

        def test_model_changes(
            self,
            generate_controller: GenerateController,
            example_existing_user_models: tuple[list, list],
        ):
            existing_models, user_models = example_existing_user_models
            to_add_result, to_remove_result = (
                generate_controller.local_extractor.model_changes(
                    existing_models, user_models
                )
            )

            to_add_valid = [("ui", "card.tsx")]
            to_remove_valid = [("ui", "input.tsx"), ("ui", "form.tsx")]
            counts = generate_controller.local_extractor.model_counts

            to_remove_result.sort()
            to_remove_valid.sort()

            checks = [
                to_add_result == to_add_valid,
                to_remove_result == to_remove_valid,
                counts.generate == len(to_add_valid),
                counts.remove == len(to_remove_valid),
            ]

            assert all(checks), (checks, to_remove_result)

        def test_store_models(
            self,
            generate_controller: GenerateController,
            example_existing_user_models: tuple[list, list],
        ):
            existing_models, user_models = example_existing_user_models
            to_add_result, to_remove_result = (
                generate_controller.local_extractor.model_changes(
                    existing_models, user_models
                )
            )

            existing_models.sort()
            to_remove_result.sort()

            generate_controller.store_models(
                existing_models, to_add_result, to_remove_result
            )

            existing_valid = [
                ("ui", "input.tsx"),
                ("ui", "form.tsx"),
                ("uploadthing", "file-upload.tsx"),
            ]
            remove_valid = [("ui", "form.tsx"), ("ui", "input.tsx")]

            existing_valid.sort()
            remove_valid.sort()

            valid_dict = {
                "existing": existing_valid,
                "generate": [("ui", "card.tsx")],
                "remove": remove_valid,
            }
            valid_dict["counts"] = CountStorage(
                generate=len(valid_dict["generate"]),
                remove=len(valid_dict["remove"]),
            )

            assert generate_controller.storage.components == ModelFileStorage(
                **valid_dict
            )

    class TestRetrieveAssets:
        @staticmethod
        def test_asset_retrieval_basic(generate_controller: GenerateController):
            generate_controller.storage.components.counts.generate = 1
            generate_controller.local_builder.components.generate = [
                ("ui", "accordion.tsx")
            ]
            dirpath = os.path.join(generate_controller.paths.components, "ui")
            generate_controller.retrieve_assets()

            assert os.path.exists(os.path.join(dirpath, "accordion.tsx"))

        @staticmethod
        def test_asset_retrieval_ut(generate_controller: GenerateController):
            # TODO: complete
            pass

        @staticmethod
        def test_count_zero(generate_controller: GenerateController):
            generate_controller.retrieve_assets()

    class TestRemoveModels:
        @staticmethod
        def test_model_removal_basic(generate_controller: GenerateController):
            generate_controller.storage.components.counts.remove = 1
            generate_controller.local_builder.components.remove = [
                ("ui", "accordion.tsx")
            ]
            dirpath = os.path.join(generate_controller.paths.components, "ui")
            file1 = os.path.join(dirpath, "accordion.tsx")
            os.makedirs(dirpath)

            with open(file1, "w") as f:
                f.write("test")

            generate_controller.remove_models()

            assert not os.path.exists(os.path.join(dirpath, "accordion.tsx"))

        @staticmethod
        def test_model_removal_ut(generate_controller: GenerateController):
            # TODO: complete
            pass

        @staticmethod
        def test_count_zero(generate_controller: GenerateController):
            generate_controller.remove_models()

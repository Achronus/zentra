import os
import pytest
import typer

from zentra_models.cli.constants import GITHUB_INIT_ASSETS_DIR
from zentra_models.cli.local.storage import ConfigExistStorage, SetupPathStorage

from zentra_models.cli.commands.setup import SetupController

from tests.mappings.retrieval import ZENTRA_INIT_VALID
from zentra_models.core import Page, Zentra
from zentra_models.ui import Form, FormField
from zentra_models.ui.control import Input
from zentra_models.ui.notification import AlertDialog
from zentra_models.ui.presentation import Card
from zentra_models.uploadthing import FileUpload


@pytest.fixture
def setup_controller(tmp_path) -> SetupController:
    return SetupController(
        url=GITHUB_INIT_ASSETS_DIR,
        paths=SetupPathStorage(
            config=os.path.join(tmp_path, "zentra_models", "zentra_init.py"),
            models=os.path.join(tmp_path, "zentra_models"),
            demo=os.path.join(tmp_path, "zentra_config", "_demo"),
        ),
        config_exists=ConfigExistStorage(),
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


class TestSetupController:
    @staticmethod
    def test_make_models_dir_true(setup_controller: SetupController):
        setup_controller.config_exists.models_folder_exists = True
        setup_controller._make_models_dir()

        assert not os.path.exists(setup_controller.paths.models)

    @staticmethod
    def test_make_models_dir_false(setup_controller: SetupController):
        setup_controller.config_exists.models_folder_exists = False
        setup_controller._make_models_dir()

        assert os.path.exists(setup_controller.paths.models)

    @staticmethod
    def test_make_config_file_true(setup_controller: SetupController):
        setup_controller.config_exists.config_file_exists = True
        setup_controller._make_config_file()

        assert not os.path.exists(setup_controller.paths.config)

    @staticmethod
    def test_make_config_file_false(setup_controller: SetupController):
        os.makedirs(setup_controller.paths.models, exist_ok=True)

        setup_controller.config_exists.config_file_exists = False
        setup_controller.retrieve_assets()
        setup_controller._make_config_file()

        assert os.path.exists(setup_controller.paths.config)

    @staticmethod
    def test_create_missing_files(setup_controller: SetupController):
        try:
            setup_controller.create_missing_files()
        except typer.Exit:
            assert False

    @staticmethod
    def test_retrieve_assets(setup_controller: SetupController):
        setup_controller.retrieve_assets()
        storage = setup_controller.config_storage

        checks = [
            storage.config == ZENTRA_INIT_VALID["config"],
            storage.demo_dir_path == ZENTRA_INIT_VALID["demo_dir_path"],
            storage.demo_filenames == ZENTRA_INIT_VALID["demo_filenames"],
        ]
        assert all(checks)

    @staticmethod
    def test_create_demo_files(setup_controller: SetupController):
        setup_controller.retrieve_assets()
        setup_controller.create_demo_files()

        filenames = setup_controller.config_storage.demo_filenames
        dest_path = setup_controller.paths.demo

        checks = [
            os.path.exists(setup_controller.paths.demo),
            os.path.exists(os.path.join(dest_path, filenames[0])),
            os.path.exists(os.path.join(dest_path, filenames[1])),
            os.path.exists(os.path.join(dest_path, filenames[2])),
        ]
        assert all(checks)

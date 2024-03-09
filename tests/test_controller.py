import os
import pytest
import typer
from cli.conf.checks import check_folder_exists

from cli.conf.constants import LocalUploadthingFilepaths, ZentaFilepaths
from cli.conf.format import name_from_camel_case
from cli.tasks.controllers.base import status, BaseController
from cli.tasks.controllers.setup import SetupController
from cli.tasks.controllers.generate import GenerateController

from zentra.core import Page, Zentra
from zentra.ui import FileUpload, Form, FormField
from zentra.ui.control import Input
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


class TestFolderDoesNotExistController:
    @pytest.fixture
    def controller(self) -> SetupController:
        return SetupController()

    def test_make_path_success(self, controller: SetupController):
        result, e = controller.make_path()
        assert result is True and e is None


class TestNameStorage:
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


class TestGenerateController:
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
    def controller(self, zentra: Zentra) -> GenerateController:
        return GenerateController(zentra)

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

    class TestCheckConfig:
        def test_success(self, tmp_path, controller: GenerateController):
            config_path = os.path.join(tmp_path, "config_file.py")
            with open(config_path, "w") as f:
                f.write(
                    "\nfrom zentra.core import Zentra\nzentra = Zentra()\nzentra.register()"
                )

            assert controller.check_config() == (True, None)

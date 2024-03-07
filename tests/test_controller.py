import pytest

from cli.conf.constants import LocalUploadthingFilepaths
from cli.conf.format import name_from_camel_case
from cli.tasks.controllers.base import status, BaseController
from cli.tasks.controllers.path import FolderDoesNotExistController
from cli.tasks.controllers.generate import GenerateController

from zentra.core import Page, Zentra
from zentra.ui import FileUpload, Form, FormField
from zentra.ui.control import Input
from zentra.ui.notification import AlertDialog
from zentra.ui.presentation import Card

from rich.progress import Progress


class TestStatus:
    def test_success(self):
        @status
        def success_task():
            pass

        result = success_task()
        assert result is True

    def test_fail(self):
        @status
        def failing_task():
            raise ValueError("Test exception in 'test_controller.py' -> 'TestStatus'")

        result = failing_task()
        assert result is False


class TestBaseController:
    def test_format_tasks(self):
        tasks = [(None, "Task 1"), (None, "Task 2")]
        controller = BaseController(tasks=tasks)
        controller.format_tasks()

        valid_tasks = [(None, "   Task 1..."), (None, "   Task 2...")]
        assert controller.tasks == valid_tasks

    def test_run(self):
        tasks = [(lambda: True, "Task 1"), (lambda: False, "Task 2")]
        controller = BaseController(tasks=tasks)
        controller.run(Progress())
        assert all(
            [
                len(controller.called_tasks) == 2,
                controller.called_tasks[0] == ("   Task 1...", True),
                controller.called_tasks[1] == ("   Task 2...", False),
            ]
        ), controller.called_tasks


class TestFolderDoesNotExistController:
    @pytest.fixture
    def controller(self) -> FolderDoesNotExistController:
        return FolderDoesNotExistController()

    def test_make_path_success(self, controller: FolderDoesNotExistController):
        assert controller.make_path() is True


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

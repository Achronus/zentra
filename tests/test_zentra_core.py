from pydantic import ValidationError
import pytest
from zentra.core import Zentra, Page, Component
from zentra.ui import Form, FormField
from zentra.ui.control import Input
from zentra.ui.notification import AlertDialog
from zentra.ui.presentation import Card
from zentra.uploadthing import FileUpload


class TestComponent:
    @staticmethod
    def test_attr_str():
        assert Component().attr_str() is None

    @staticmethod
    def test_content_str():
        assert Component().content_str() is None

    @staticmethod
    def test_unique_logic_str():
        assert Component().unique_logic_str() is None

    @staticmethod
    def test_below_content_str():
        assert Component().below_content_str() is None


class TestZentra:
    @pytest.fixture
    def zentra(self) -> Zentra:
        return Zentra()

    @pytest.fixture
    def form_fields(self) -> list[FormField | list[FormField]]:
        return [
            FormField(
                name="agencyLogo",
                label="Agency Logo",
                content=FileUpload(),
            ),
            [
                FormField(
                    name="name",
                    label="Agency Name",
                    content=Input(
                        id="agencyName",
                        type="text",
                        placeholder="Your Agency Name",
                    ),
                ),
                FormField(
                    name="companyEmail",
                    label="Agency Email",
                    content=Input(
                        id="email",
                        type="email",
                        placeholder="Email",
                    ),
                ),
            ],
        ]

    @pytest.fixture
    def page(self, form_fields) -> Page:
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
                                    fields=form_fields,
                                    btn_text="Save Agency Information",
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    @pytest.fixture
    def zentra_registered(self, page: Page) -> Zentra:
        zentra = Zentra()
        zentra.register([page])
        return zentra

    def test_init(self, zentra: Zentra):
        assert zentra.pages == []
        assert zentra.components == []

    def test_init_fail(self):
        with pytest.raises(ValidationError):
            Zentra(pages=["test"])

    def test_page_registration(self, zentra: Zentra):
        page1 = Page(
            name="Page1",
            components=[
                Input(id="test1", type="text", placeholder="Component1"),
            ],
        )
        page2 = Page(
            name="Page2",
            components=[
                Input(id="test2", type="text", placeholder="Component2"),
            ],
        )
        page_map = [page1, page2]
        zentra.register(page_map)

        assert zentra.pages == page_map
        assert zentra.components == []

    def test_register_components(self, zentra: Zentra):
        component1 = Component(name="Component1")
        component2 = Component(name="Component2")
        standalone_components = [component1, component2]
        zentra.register(standalone_components)

        assert zentra.pages == []
        assert zentra.components == standalone_components

    def test_mixed_registration(self, zentra: Zentra):
        page = Page(
            name="Page1",
            components=[
                Input(id="test", type="text", placeholder="Component1"),
            ],
        )
        component = Input(id="test", type="text", placeholder="Component1")
        mixed_list = [page, component]
        zentra.register(mixed_list)

        assert zentra.pages == [page]
        assert zentra.components == [component]

    def test_register_invalid_input(self, zentra: Zentra):
        invalid_input = "InvalidInput"
        with pytest.raises(ValueError):
            zentra.register(invalid_input)

    def test_storage_valid(self, zentra_registered: Zentra):
        storage = zentra_registered.name_storage

        storage.components.sort()
        storage.filenames.sort()

        valid_components = ["AlertDialog", "Card", "FileUpload", "Form", "Input"]
        valid_filenames = [
            ("ui", "alert-dialog.tsx"),
            ("ui", "card.tsx"),
            ("uploadthing", "file-upload.tsx"),
            ("ui", "form.tsx"),
            ("ui", "input.tsx"),
        ]

        valid_components.sort()
        valid_filenames.sort()

        checks = [
            storage.pages == ["AgencyDetails"],
            storage.components == valid_components,
            storage.filenames == valid_filenames,
        ]
        assert all(checks), checks

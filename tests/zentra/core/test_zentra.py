import pytest

from zentra_models.core import Zentra, Page, Component
from zentra_models.ui import Form, FormField
from zentra_models.ui.control import Input
from zentra_models.ui.notification import AlertDialog
from zentra_models.ui.presentation import Card
from zentra_models.uploadthing import FileUpload


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
        zentra.models.register([page])
        return zentra

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
        zentra.models.register(page_map)

        assert zentra.models.pages == page_map
        assert zentra.models.components == []

    def test_register_components(self, zentra: Zentra):
        component1 = Component(name="Component1")
        component2 = Component(name="Component2")
        standalone_components = [component1, component2]
        zentra.models.register(standalone_components)

        assert zentra.models.pages == []
        assert zentra.models.components == standalone_components

    def test_mixed_registration(self, zentra: Zentra):
        page = Page(
            name="Page1",
            components=[
                Input(id="test", type="text", placeholder="Component1"),
            ],
        )
        component = Input(id="test", type="text", placeholder="Component1")
        mixed_list = [page, component]
        zentra.models.register(mixed_list)

        assert zentra.models.pages == [page]
        assert zentra.models.components == [component]

    def test_register_invalid_input(self, zentra: Zentra):
        invalid_input = "InvalidInput"
        with pytest.raises(ValueError):
            zentra.models.register(invalid_input)

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

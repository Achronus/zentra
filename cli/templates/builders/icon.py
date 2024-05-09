from cli.templates.builders.jsx import AttributeBuilder
from cli.templates.ui.mappings.storage import AttributeMappings
from cli.templates.utils import compress, text_content
from zentra.core.react import LucideIcon, LucideIconWithText


class IconBuilder:
    """A builder for creating the JSX for `LucideIcon` Zentra models."""

    def __init__(
        self,
        model: LucideIcon | LucideIconWithText,
        mappings: AttributeMappings,
    ) -> None:
        self.model = model

        self.attrs = AttributeBuilder(
            component=model,
            common_mapping=mappings.common,
            component_mapping=mappings.model,
        )

    def build(self) -> tuple[list[str], str]:
        """Creates the JSX for the model and return its details as a tuple in the form of: `(content, import_str)`."""
        content = self.create_container()

        if isinstance(self.model, LucideIconWithText):
            content = self.handle_text(content)

        return content, self.model.import_str

    def handle_text(self, content: list[str]) -> list[str]:
        """Manages the text location and preprocessing inside the `content` list. Returns the updated list."""
        if self.model.text:
            self.model.text = text_content(self.model.text)[0]
            if self.model.position == "start":
                content.append(self.model.text)
            else:
                content.insert(0, self.model.text)

        return content

    def create_container(self) -> list[str]:
        """Creates the icon container and applies the attributes to it. Returns it as a list of strings."""
        attrs_str = compress(self.attrs.build(), chars=" ")
        return [
            f'<{self.model.name} className="mr-2 h-4 w-4"{f' {attrs_str}' if attrs_str else ''} />'
        ]

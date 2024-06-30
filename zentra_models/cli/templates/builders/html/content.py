from zentra_models.cli.templates.builders.html.utils import get_html_content
from zentra_models.cli.templates.storage import JSXComponentExtras

from zentra_models.cli.templates.ui.mappings.storage import HTMLShellMappings

from zentra_models.core.html import HTMLContent


class HTMLContentBuilder:
    """A builder for creating the `HTMLContent` Zentra HTML model content as JSX."""

    def __init__(self, model: HTMLContent, mappings: HTMLShellMappings) -> None:
        self.model = model
        self.maps = mappings

        self.storage = JSXComponentExtras()

    def build(self) -> tuple[list[str], JSXComponentExtras]:
        """Builds the JSX content and returns it as a tuple in the form: `(content, storage)`."""
        content = get_html_content(model=self.model, mappings=self.maps)
        return content, self.storage

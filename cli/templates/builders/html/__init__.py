from cli.templates.builders import add_to_storage
from cli.templates.builders.html.content import HTMLContentBuilder
from cli.templates.builders.html.div import DivBuilder
from cli.templates.builders.html.figure import FigureBuilder

from cli.templates.storage import JSXComponentExtras

from cli.templates.ui.mappings.storage import DivMappings
from zentra.core.base import HTMLTag
from zentra.core.html import Div, Figure, HTMLContent


class HTMLBuildController:
    """A build controller for creating Zentra `HTMLTag` models as JSX."""

    def __init__(self, model: HTMLTag, mappings: DivMappings) -> None:
        self.model = model
        self.maps = mappings

        self.storage = JSXComponentExtras()

    def build(self) -> tuple[list[str], JSXComponentExtras]:
        """Builds the models JSX content and returns it as a tuple in the form: `(content, storage)`"""

        if isinstance(self.model, Div):
            builder = DivBuilder(model=self.model, mappings=self.maps)
        elif isinstance(self.model, HTMLContent):
            builder = HTMLContentBuilder(self.model, self.maps.html_shell)

        elif isinstance(self.model, Figure):
            builder = FigureBuilder(model=self.model, mappings=self.maps.figure)
        else:
            raise TypeError(f"'{type(self.model)}' not supported.")

        content, storage = builder.build()
        self.storage = add_to_storage(self.storage, storage, extend=True)
        return content, self.storage

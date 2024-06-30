from zentra_models.cli.templates.builders import add_to_storage
from zentra_models.cli.templates.builders.html.content import HTMLContentBuilder
from zentra_models.cli.templates.builders.html.figure import FigureBuilder
from zentra_models.cli.templates.builders.html.utils import get_html_content

from zentra_models.cli.templates.storage import (
    JSXComponentContentStorage,
    JSXComponentExtras,
)
from zentra_models.cli.templates.ui.content import text_content

from zentra_models.cli.templates.ui.mappings.storage import DivMappings
from zentra_models.cli.templates.utils import str_to_list

from zentra_models.core import Component
from zentra_models.base.html import HTMLTag
from zentra_models.base.js import JSIterable
from zentra_models.core.html import Div, Figure, HTMLContent


class DivBuilder:
    """A builder for creating the `Div` Zentra HTML model content as JSX."""

    def __init__(self, model: Div, mappings: DivMappings) -> None:
        self.model = model
        self.maps = mappings

        self.storage = JSXComponentExtras()
        self.inner_content = []

    def build(self) -> tuple[list[str], JSXComponentExtras]:
        """Builds the JSX content and returns it as a tuple in the form: `(content, storage)`."""
        if not isinstance(self.model.items, list):
            self.model.items = [self.model.items]

        shell_start, shell_end = get_html_content(self.model, self.maps.html_shell)
        self.build_content(self.model.items)
        content = [shell_start, *self.inner_content, shell_end]

        return content, self.storage

    def build_js_iterable(
        self, model: JSIterable
    ) -> tuple[list[str], JSXComponentExtras]:
        """Creates the JSX for a `JSIterable` model and returns its details as a tuple in the form of `(content, multi_comp_storage)`."""
        from zentra_models.cli.templates.builders.js import JSIterableBuilder
        from zentra_models.cli.templates.ui.mappings.storage import JSIterableMappings

        builder = JSIterableBuilder(
            model=model,
            mappings=JSIterableMappings(
                component=self.maps.component,
                html=self.maps,
            ),
        )
        content = builder.build()
        return content, builder.comp_storage

    def build_component(
        self, component: Component, full_shell: bool = False
    ) -> tuple[list[str], JSXComponentContentStorage]:
        """Creates the JSX for a `Component` model and returns its details as a tuple in the form of `(content, comp_storage)`."""
        from zentra_models.cli.templates.builders.component import ComponentBuilder

        builder = ComponentBuilder(component=component, mappings=self.maps.component)
        builder.build(full_shell=full_shell)
        return str_to_list(builder.storage.content), builder.storage

    def build_content(
        self,
        item: str
        | Component
        | JSIterable
        | list[str | HTMLTag | Component | JSIterable],
    ) -> None:
        """Builds the content for the `Div` model and stores the content in `self.inner_content` and any component information in `self.storage`."""
        if isinstance(item, JSIterable):
            content, storage = self.build_js_iterable(model=item)
            self.inner_content.extend(content)
            self.storage = add_to_storage(self.storage, storage, extend=True)

        elif isinstance(item, Component):
            content, storage = self.build_component(component=item)
            self.inner_content.extend(content)
            self.storage = add_to_storage(self.storage, storage)

        elif isinstance(item, Figure):
            builder = FigureBuilder(model=item, mappings=self.maps.figure)
            content, storage = builder.build()
            self.inner_content.extend(content)
            self.storage = add_to_storage(self.storage, storage, extend=True)

        elif isinstance(item, HTMLContent):
            content, _ = HTMLContentBuilder(
                model=item,
                mappings=self.maps.html_shell,
            ).build()
            self.inner_content.extend(content)

        elif isinstance(item, Div):
            shell_start, shell_end = get_html_content(item, self.maps.html_shell)
            self.inner_content.append(shell_start)
            self.build_content(item.items)
            self.inner_content.append(shell_end)

        elif isinstance(item, str):
            self.inner_content.extend(text_content(item))

        elif isinstance(item, list):
            for i in item:
                self.build_content(item=i)

        else:
            raise TypeError(f"'{type(item)}' not supported.")

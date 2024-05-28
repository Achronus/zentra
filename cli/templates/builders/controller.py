from cli.templates.storage import JSXComponentContentStorage, JSXComponentExtras
from cli.templates.ui.mappings.storage import ControllerMappings
from cli.templates.utils import str_to_list

from zentra.core import Component
from zentra.core.base import HTMLTag, JSIterable
from zentra.core.react import LucideIcon


class BuildController:
    """A controller for selecting Zentra model JSX builders."""

    def __init__(self, mappings: ControllerMappings) -> None:
        self.maps = mappings

    def build_component(
        self, component: Component, full_shell: bool = False
    ) -> tuple[list[str], JSXComponentContentStorage]:
        """Creates the JSX for a `Component` model and returns its details as a tuple in the form of `(content, comp_storage)`."""
        from cli.templates.builders.component import ComponentBuilder

        builder = ComponentBuilder(component=component, mappings=self.maps.component)
        builder.build(full_shell=full_shell)
        return str_to_list(builder.storage.content), builder.storage

    def build_nextjs_component(
        self, component: Component
    ) -> tuple[list[str], JSXComponentContentStorage]:
        """Creates the JSX for a `NextJS` model and returns its details as a tuple in the form of `(content, comp_storage)`."""
        from cli.templates.builders.nextjs import NextJSComponentBuilder

        nextjs = NextJSComponentBuilder(
            component=component, mappings=self.maps.component
        )
        nextjs.build()
        return str_to_list(nextjs.storage.content), nextjs.storage

    def build_js_iterable(
        self, model: JSIterable
    ) -> tuple[list[str], JSXComponentExtras]:
        """Creates the JSX for a `JSIterable` model and returns its details as a tuple in the form of `(content, multi_comp_storage)`."""
        from cli.templates.builders.js import JSIterableBuilder

        builder = JSIterableBuilder(model=model, mappings=self.maps.js_iterable)
        content = builder.build()
        return content, builder.comp_storage

    def build_html_tag(self, model: HTMLTag) -> tuple[list[str], JSXComponentExtras]:
        """Creates the JSX for a `HTMLTag` model and returns its details as a tuple in the form of `(content, multi_comp_storage)`."""
        from cli.templates.builders.html import HTMLBuildController

        builder = HTMLBuildController(model=model, mappings=self.maps.html)
        content, storage = builder.build()
        return content, storage

    def build_icon(self, model: LucideIcon) -> tuple[list[str], str]:
        """Creates the JSX for a `LucideIcon` model and returns its details as a tuple in the form of: `(content, import_str)`."""
        from cli.templates.builders.icon import IconBuilder

        builder = IconBuilder(model=model, mappings=self.maps.component.attribute)
        content, import_str = builder.build()
        return content, import_str

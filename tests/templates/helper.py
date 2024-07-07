from zentra_models.templates.builders.component import ComponentBuilder
from zentra_models.templates.builders.structural import JSXPageBuilder

from zentra_models.templates.ui.mappings import COMPONENT_MAPPINGS, JSX_MAPPINGS

from zentra_models.core import Component, ReactFile


def component_builder(component: Component) -> ComponentBuilder:
    return ComponentBuilder(component, mappings=COMPONENT_MAPPINGS)


def page_builder(page: ReactFile) -> JSXPageBuilder:
    return JSXPageBuilder(page=page, mappings=JSX_MAPPINGS)


class SimpleCompBuilder:
    """A helper class that handles the logic for keeping simple component test implementations unified."""

    def __init__(self, component: Component) -> None:
        self.component = component

    def run(self, result_attr: str, valid_value: str, list_output: bool = False):
        builder = component_builder(self.component)
        builder.build()

        result: str = getattr(builder.storage, result_attr)

        if list_output:
            result = result.split("\n")

        assert result == valid_value, (
            result if list_output else result.split("\n"),
            valid_value if list_output else valid_value.split("\n"),
        )

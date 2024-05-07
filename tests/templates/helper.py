from cli.conf.storage import ComponentDetails
from cli.templates.jsx import (
    BuildController,
    ComponentBuilder,
    HTMLContentBuilder,
    JSIterableContentBuilder,
    JSXPageBuilder,
    NextJSComponentBuilder,
    ParentComponentBuilder,
)
from cli.templates.mappings import JSX_MAPPINGS
from tests.templates.details import COMPONENT_DETAILS_MAPPING, component_details
from zentra.core import Component, Page
from zentra.core.base import HTMLTag, JSIterable


def build_controller() -> BuildController:
    return BuildController(
        mappings=JSX_MAPPINGS,
        details_dict=COMPONENT_DETAILS_MAPPING,
    )


def component_builder(
    component: Component, details: ComponentDetails
) -> ComponentBuilder:
    return ComponentBuilder(component, mappings=JSX_MAPPINGS, details=details)


def parent_component_builder(component: Component) -> ParentComponentBuilder:
    return ParentComponentBuilder(
        component,
        mappings=JSX_MAPPINGS,
        details_dict=COMPONENT_DETAILS_MAPPING,
    )


def nextjs_component_builder(component: Component) -> NextJSComponentBuilder:
    return NextJSComponentBuilder(component, mappings=JSX_MAPPINGS)


def html_content_builder(model: HTMLTag) -> HTMLContentBuilder:
    return HTMLContentBuilder(
        model=model,
        mappings=JSX_MAPPINGS,
        details_dict=COMPONENT_DETAILS_MAPPING,
    )


def js_iterable_content_builder(model: JSIterable) -> JSIterableContentBuilder:
    return JSIterableContentBuilder(
        model=model,
        mappings=JSX_MAPPINGS,
        details_dict=COMPONENT_DETAILS_MAPPING,
    )


def page_builder(page: Page) -> JSXPageBuilder:
    return JSXPageBuilder(page=page, mappings=JSX_MAPPINGS, details=component_details())


class SimpleCompBuilder:
    """A helper class that handles the logic for keeping simple component test implementations unified."""

    def __init__(
        self, component: Component, component_details: ComponentDetails
    ) -> None:
        self.component = component
        self.details = component_details

    def run(self, result_attr: str, valid_value: str, list_output: bool = False):
        builder = component_builder(self.component, details=self.details)
        builder.build()

        result: str = getattr(builder.storage, result_attr)

        if list_output:
            result = result.split("\n")

        assert result == valid_value, (
            result if list_output else result.split("\n"),
            valid_value if list_output else valid_value.split("\n"),
        )


class ParentCompBuilder:
    """A helper class that handles the logic for keeping parent component test implementations unified."""

    def __init__(
        self,
        component: Component,
    ) -> None:
        self.component = component

        self.builder = parent_component_builder(component)

    def content(self, valid_value: str):
        result: list[str] = self.builder.build()
        assert "\n".join(result) == valid_value, (result, valid_value.split("\n"))

    def comp_other(self, result_attr: str, valid_value: str, list_output: bool = False):
        _ = self.builder.build()
        result: list[str] = getattr(self.builder.storage, result_attr)
        if list_output:
            assert result == valid_value, (result, valid_value.split("\n"))
        else:
            assert "\n".join(result) == valid_value, (result, valid_value.split("\n"))

from cli.templates.builders.component import ComponentBuilder
from cli.templates.builders.html import HTMLBuildController
from cli.templates.builders.html.figure import FigCaptionBuilder
from cli.templates.builders.icon import IconBuilder
from cli.templates.builders.js import JSIterableBuilder
from cli.templates.builders.nextjs import NextJSComponentBuilder
from cli.templates.builders.structural import JSXPageBuilder

from cli.templates.ui.mappings import (
    ATTRIBUTE_MAPPINGS,
    COMPONENT_MAPPINGS,
    DIV_MAPPINGS,
    HTML_SHELL_MAPPINGS,
    JS_ITERABLE_MAPPINGS,
    JSX_MAPPINGS,
)

from zentra.core import Component, Page
from zentra.core.base import HTMLTag, JSIterable
from zentra.core.html import FigCaption
from zentra.core.react import LucideIcon


def component_builder(component: Component) -> ComponentBuilder:
    return ComponentBuilder(component, mappings=COMPONENT_MAPPINGS)


def nextjs_component_builder(component: Component) -> NextJSComponentBuilder:
    return NextJSComponentBuilder(component, mappings=COMPONENT_MAPPINGS)


def html_content_builder(model: HTMLTag) -> HTMLBuildController:
    return HTMLBuildController(model=model, mappings=DIV_MAPPINGS)


def fig_caption_builder(model: FigCaption) -> FigCaptionBuilder:
    return FigCaptionBuilder(model=model, mappings=HTML_SHELL_MAPPINGS)


def js_iterable_content_builder(model: JSIterable) -> JSIterableBuilder:
    return JSIterableBuilder(model=model, mappings=JS_ITERABLE_MAPPINGS)


def icon_builder(model: LucideIcon) -> IconBuilder:
    return IconBuilder(model=model, mappings=ATTRIBUTE_MAPPINGS)


def page_builder(page: Page) -> JSXPageBuilder:
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

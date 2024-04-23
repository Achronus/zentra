from cli.conf.storage import ComponentDetails
from cli.templates.jsx import (
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


def component_builder(
    component: Component, details: ComponentDetails
) -> ComponentBuilder:
    return ComponentBuilder(component, mappings=JSX_MAPPINGS, details=details)


def parent_component_builder(component: Component) -> ParentComponentBuilder:
    return ParentComponentBuilder(
        component, mappings=JSX_MAPPINGS, details_dict=COMPONENT_DETAILS_MAPPING
    )


def nextjs_component_builder(component: Component) -> NextJSComponentBuilder:
    return NextJSComponentBuilder(component, mappings=JSX_MAPPINGS)


def html_content_builder(model: HTMLTag) -> HTMLContentBuilder:
    return HTMLContentBuilder(model=model, mappings=JSX_MAPPINGS)
    

def js_iterable_content_builder(model: JSIterable) -> JSIterableContentBuilder:
    return JSIterableContentBuilder(model=model, mappings=JSX_MAPPINGS)


def page_builder(page: Page) -> JSXPageBuilder:
    return JSXPageBuilder(page=page, mappings=JSX_MAPPINGS, details=component_details())

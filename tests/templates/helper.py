from cli.conf.storage import ComponentDetails
from cli.templates.jsx import ComponentBuilder, JSXPageBuilder
from cli.templates.mappings import JSX_MAPPINGS
from tests.templates.details import component_details
from zentra.core import Component, Page


def component_builder(
    component: Component, details: ComponentDetails
) -> ComponentBuilder:
    return ComponentBuilder(component, mappings=JSX_MAPPINGS, details=details)


def page_builder(page: Page) -> JSXPageBuilder:
    return JSXPageBuilder(page=page, mappings=JSX_MAPPINGS, details=component_details())

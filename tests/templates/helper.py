from cli.conf.storage import ComponentDetails
from cli.templates.jsx import ComponentBuilder, JSXPageBuilder, ParentComponentBuilder
from cli.templates.mappings import JSX_MAPPINGS
from tests.templates.details import COMPONENT_DETAILS_MAPPING, component_details
from zentra.core import Component, Page


def component_builder(
    component: Component, details: ComponentDetails
) -> ComponentBuilder:
    return ComponentBuilder(component, mappings=JSX_MAPPINGS, details=details)


def parent_component_builder(component: Component) -> ParentComponentBuilder:
    return ParentComponentBuilder(
        component, mappings=JSX_MAPPINGS, details_dict=COMPONENT_DETAILS_MAPPING
    )


def page_builder(page: Page) -> JSXPageBuilder:
    return JSXPageBuilder(page=page, mappings=JSX_MAPPINGS, details=component_details())

from cli.templates.builder import ComponentJSXBuilder
from zentra.core import Component


def builder(component: Component) -> ComponentJSXBuilder:
    return ComponentJSXBuilder(component)

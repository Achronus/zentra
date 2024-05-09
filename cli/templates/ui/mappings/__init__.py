from cli.templates.ui.mappings.maps import (
    ATTR_DICT,
    COMPONENTS_TO_WRAP,
    CONTENT_DICT,
    IMPORT_DICT,
    LOGIC_MAPPING,
    MAPPING_DICT,
    PARENT_COMPONENTS,
)
from cli.templates.ui.mappings.storage import (
    AttributeMappings,
    ComponentMappings,
    ContentMappings,
    ControllerMappings,
    DivMappings,
    FigureMappings,
    HTMLShellMappings,
    ImportMappings,
    JSIterableMappings,
    JSXMappings,
    ParentMappings,
)


JSX_MAPPINGS = JSXMappings(**MAPPING_DICT)

CONTENT_MAPPINGS = ContentMappings(**CONTENT_DICT)
ATTRIBUTE_MAPPINGS = AttributeMappings(**ATTR_DICT)
IMPORT_MAPPINGS = ImportMappings(**IMPORT_DICT)

COMPONENT_MAPPINGS = ComponentMappings(
    content=CONTENT_MAPPINGS,
    attribute=ATTRIBUTE_MAPPINGS,
    imports=IMPORT_MAPPINGS,
    logic=LOGIC_MAPPING,
    wrappers=COMPONENTS_TO_WRAP,
)

HTML_SHELL_MAPPINGS = HTMLShellMappings(
    content=CONTENT_MAPPINGS,
    attribute=ATTRIBUTE_MAPPINGS,
)

FIGURE_MAPPINGS = FigureMappings(
    nextjs=COMPONENT_MAPPINGS,
    html_shell=HTML_SHELL_MAPPINGS,
)

DIV_MAPPINGS = DivMappings(
    html_shell=HTML_SHELL_MAPPINGS,
    component=COMPONENT_MAPPINGS,
    figure=FIGURE_MAPPINGS,
)

JS_ITERABLE_MAPPINGS = JSIterableMappings(
    component=COMPONENT_MAPPINGS,
    html=DIV_MAPPINGS,
)

CONTROLLER_MAPPINGS = ControllerMappings(
    component=COMPONENT_MAPPINGS,
    js_iterable=JS_ITERABLE_MAPPINGS,
    html=DIV_MAPPINGS,
)

PARENT_MAPPINGS = ParentMappings(
    parent=PARENT_COMPONENTS,
    controller=CONTROLLER_MAPPINGS,
)

from pydantic import BaseModel
from cli.conf.types import MappingDict


class JSXMappings(BaseModel):
    """A storage container for JSX mappings."""

    common_attrs: MappingDict
    component_attrs: MappingDict
    common_content: MappingDict
    component_content: MappingDict
    common_logic: MappingDict
    additional_imports: MappingDict
    wrappers: dict[str, str]
    use_client_map: list[str]


class ContentMappings(BaseModel):
    """A storage container for JSX content mappings."""

    common: MappingDict
    model: MappingDict


class AttributeMappings(BaseModel):
    """A storage container for JSX attribute mappings."""

    common: MappingDict
    model: MappingDict


class ImportMappings(BaseModel):
    """A storage container for JSX import mappings."""

    extra: MappingDict


class ComponentMappings(BaseModel):
    """A storage container for JSX mappings associated to the `ComponentBuilder`."""

    content: ContentMappings
    attribute: AttributeMappings
    imports: ImportMappings
    logic: MappingDict
    wrappers: dict[str, str]
    client: list[str]


class HTMLShellMappings(BaseModel):
    """A storage container for JSX mappings associated to the `HTMLTag` shell."""

    content: ContentMappings
    attribute: AttributeMappings


class FigureMappings(BaseModel):
    """A storage container for JSX mappings associated to the `FigureBuilder`."""

    nextjs: ComponentMappings
    html_shell: HTMLShellMappings


class DivMappings(BaseModel):
    """A storage container for JSX mappings associated to the `DivBuilder`."""

    html_shell: HTMLShellMappings
    component: ComponentMappings
    figure: FigureMappings


class JSIterableMappings(BaseModel):
    """A storage container for JSX mappings associated to the `JSIterableBuilder`."""

    component: ComponentMappings
    html: DivMappings


class ControllerMappings(BaseModel):
    """A storage container for JSX mappings associated to the `BuildController`."""

    component: ComponentMappings
    js_iterable: JSIterableMappings
    html: DivMappings

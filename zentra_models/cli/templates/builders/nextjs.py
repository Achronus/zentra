from zentra_models.cli.templates.builders.jsx import (
    AttributeBuilder,
    ContentBuilder,
    ImportBuilder,
)
from zentra_models.cli.templates.storage import JSXComponentContentStorage
from zentra_models.cli.templates.ui.mappings.storage import ComponentMappings
from zentra_models.cli.templates.utils import compress

from zentra_models.core import Component


class NextJSComponentBuilder:
    """A builder for creating Zentra `NextJS` models as JSX."""

    def __init__(self, component: Component, mappings: ComponentMappings) -> None:
        self.component = component
        self.wrapper_map = mappings.wrappers

        self.storage = JSXComponentContentStorage()
        self.attrs = AttributeBuilder(
            component=component,
            common_mapping=mappings.attribute.common,
            component_mapping=mappings.attribute.model,
        )
        self.import_builder = ImportBuilder(
            component=component, additional_imports_mapping=mappings.imports.extra
        )
        self.content = ContentBuilder(
            model=component,
            model_mapping=mappings.content.model,
            common_mapping=mappings.content.common,
        )

    def build(self) -> None:
        """Builds the JSX for the component."""
        self.storage.imports = compress(self.imports())
        self.storage.attributes = compress(self.attrs.build(), chars=" ")
        self.storage.content = compress(
            self.apply_content_containers(content=self.content.build())
        )

    def imports(self) -> list[str]:
        """Builds the imports based on the component attributes and mappings."""
        imports = [self.core_import()]
        extra_imports = self.import_builder.additional_imports()

        if extra_imports:
            imports.extend(extra_imports)

        return imports

    def core_import(self) -> str:
        """Creates the core import statement for the component."""
        name = self.component.container_name
        return f"import {name} from 'next/{name.lower()}'"

    def apply_content_containers(self, content: list[str]) -> list[str]:
        """Wraps the components content in its outer shell and any additional wrappers (if applicable)."""
        wrapped_content = [
            f"<{self.component.container_name}{f' {self.storage.attributes}' if self.storage.attributes else ''} />"
        ]

        if len(content) > 0:
            wrapped_content[0] = wrapped_content[0].replace(" />", ">")
            wrapped_content.extend(
                [
                    *content,
                    f"</{self.component.container_name}>",
                ]
            )

        if self.component.classname in self.wrapper_map.keys():
            wrapped_content = [
                f"<div {self.wrapper_map[self.component.classname]}>",
                *wrapped_content,
                "</div>",
            ]

        return wrapped_content

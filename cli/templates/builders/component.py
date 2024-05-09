from cli.conf.storage import ComponentDetails
from cli.templates.builders.jsx import (
    AttributeBuilder,
    ContentBuilder,
    ImportBuilder,
    LogicBuilder,
)
from cli.templates.storage import JSXComponentContentStorage
from cli.templates.ui.mappings.storage import ComponentMappings
from cli.templates.utils import compress

from zentra.core import Component


class ComponentBuilder:
    """A builder for creating Zentra `Component` models as JSX."""

    def __init__(
        self,
        component: Component,
        mappings: ComponentMappings,
        details: ComponentDetails,
    ) -> None:
        self.component = component
        self.details = details
        self.wrapper_map = mappings.wrappers

        self.storage = JSXComponentContentStorage()
        self.attrs = AttributeBuilder(
            component=component,
            common_mapping=mappings.attribute.common,
            component_mapping=mappings.attribute.model,
        )
        self.imports = ImportBuilder(
            component=component,
            additional_imports_mapping=mappings.imports.extra,
            use_state_mapping=mappings.imports.use_state,
            core_name=details.name,
            child_names=details.child_names,
        )
        self.logic = LogicBuilder(
            component=component,
            logic_mapping=mappings.logic,
        )
        self.content = ContentBuilder(
            model=component,
            model_mapping=mappings.content.model,
            common_mapping=mappings.content.common,
        )

    def build(self, full_shell: bool = False) -> None:
        """Builds the JSX for the component."""
        self.storage.imports = compress(self.imports.build())
        self.storage.attributes = compress(self.attrs.build(), chars=" ")
        self.storage.logic = compress(self.logic.build())
        self.storage.content = compress(
            self.apply_content_containers(
                content=self.content.build(), full_shell=full_shell
            )
        )

    def apply_content_containers(
        self, content: list[str], full_shell: bool
    ) -> list[str]:
        """Wraps the components content in its outer shell and any additional wrappers (if applicable)."""
        wrapped_content = [
            f"<{self.component.container_name}{f' {self.storage.attributes}' if self.storage.attributes else ''} />"
        ]

        if len(content) > 0 or full_shell:
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
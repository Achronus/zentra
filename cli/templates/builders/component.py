from cli.conf.storage import ComponentDetails
from cli.templates.builders.jsx import (
    AttributeBuilder,
    ContentBuilder,
    ImportBuilder,
    LogicBuilder,
)
from cli.templates.storage import JSXComponentContentStorage, JSXComponentExtras
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
        self.parent_map = mappings.parents
        self.use_client_map = mappings.client

        self.storage = JSXComponentContentStorage()
        self.attrs = AttributeBuilder(
            component=component,
            common_mapping=mappings.attribute.common,
            component_mapping=mappings.attribute.model,
        )
        self.imports = ImportBuilder(
            component=component,
            additional_imports_mapping=mappings.imports.extra,
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

        if self.component.classname in self.parent_map:
            content, storage_extras = self.content.build()
            self.add_extra_storage(storage_extras)
        else:
            content = self.content.build()

        self.add_use_state(self.storage.logic)
        self.add_use_client()

        self.storage.content = compress(
            self.apply_content_containers(content=content, full_shell=full_shell)
        )

    def add_extra_storage(self, storage_extras: JSXComponentExtras) -> None:
        """Adds the extra storage items to `self.storage`."""

        def add_item(local_item: str, item: list[str]) -> str:
            if len(item) > 0:
                local_item += "\n" + compress(item)
            return local_item

        self.storage.imports = add_item(self.storage.imports, storage_extras.imports)
        self.storage.logic = add_item(self.storage.logic, storage_extras.logic)

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

    def add_use_state(self, logic: str) -> None:
        """Adds React's `useState` import if the component requires it."""
        if "useState" in logic:
            import_str = 'import { useState } from "react"\n'
            self.storage.imports = import_str + self.storage.imports

    def add_use_client(self) -> None:
        """Adds NextJS's `use client` import if the component requires it."""
        if self.component.classname in self.use_client_map:
            import_str = '"use client"\n'
            self.storage.imports = import_str + self.storage.imports

from cli.templates.builders.jsx import (
    AttributeBuilder,
    ContentBuilder,
    ImportBuilder,
    LogicBuilder,
)
from cli.templates.storage import JSXComponentContentStorage, JSXComponentExtras
from cli.templates.ui.mappings.storage import ComponentMappings
from cli.templates.utils import compress, compress_imports, str_to_list

from zentra.core import Component


class ComponentBuilder:
    """A builder for creating Zentra `Component` models as JSX."""

    def __init__(
        self,
        component: Component,
        mappings: ComponentMappings,
    ) -> None:
        self.component = component
        self.wrapper_map = mappings.wrappers
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

        content = self.content.build()

        if isinstance(content, tuple):
            content, storage_extras = content
            self.add_extra_storage(storage_extras)

        self.storage.content = compress(
            self.apply_content_containers(content=content, full_shell=full_shell)
        )

        if self.component.child_names:
            self.storage.imports = self.tidy_child_names(
                self.storage.imports,
                self.storage.content,
            )

        self.storage.imports = self.handle_imports(
            self.storage.logic,
            self.storage.imports,
        )

    def add_extra_storage(self, storage_extras: JSXComponentExtras) -> None:
        """Adds the extra storage items to `self.storage`."""

        def add_item(local_item: str, item: list[str]) -> str:
            if len(item) > 0:
                local_item += "\n" + compress(item)
            return local_item.lstrip("\n")

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
            value = self.wrapper_map[self.component.classname]

            if isinstance(value, tuple):
                if getattr(self.component, value[0]) != value[1]:
                    return wrapped_content

                value = value[-1]

            wrapped_content = [
                f"<div {value}>",
                *wrapped_content,
                "</div>",
            ]

        return wrapped_content

    def add_use_state(self, logic: str, imports: str) -> str:
        """Adds React's `useState` import if the component requires it."""
        if "useState" in logic:
            import_str = 'import { useState } from "react"\n'
            return import_str + imports

        return imports

    def add_use_client(self, logic: str, imports: str) -> str:
        """Adds NextJS's `use client` import if the component requires it."""
        if self.component.classname in self.use_client_map or "useState" in logic:
            import_str = '"use client"\n'
            return import_str + imports

        return imports

    def tidy_child_names(self, imports: str, content: str) -> str:
        """Removes component child names from the import statements, if they are not used in the components content."""
        used_child_names = []
        for name in self.component.child_names:
            if name in content:
                used_child_names.append(name)

        imports_list = str_to_list(imports)
        for idx, import_str in enumerate(imports_list):
            if self.component.container_name in import_str:
                imports_list.pop(idx)
                break

        used_child_names.sort()
        imports_list.insert(0, self.imports.core_import(used_child_names))
        return compress(imports_list)

    def handle_imports(self, logic: str, imports: str) -> str:
        """Performs import processing such as adding in additional imports and compressing them. Returns the updated version as a string."""
        imports = self.add_use_state(logic, imports)
        imports = compress(compress_imports(str_to_list(imports)))
        imports = self.add_use_client(logic, imports)
        return imports

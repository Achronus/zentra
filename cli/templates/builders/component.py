from cli.conf.storage import ComponentDetails
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

        self.storage.content = compress(
            self.apply_content_containers(content=content, full_shell=full_shell)
        )

        self.storage.imports = self.tidy_child_names(
            self.details.child_names,
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

    def tidy_child_names(
        self, child_names: list[str], imports: str, content: str
    ) -> str:
        """Removes component child names from the import statements, if they are not used in the components content."""
        used_child_names = []
        for name in child_names:
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
        imports = compress(compress_imports(str_to_list(imports)))
        imports = self.add_use_state(logic, imports)
        imports = self.add_use_client(logic, imports)
        return imports

from cli.conf.storage import ComponentDetails
from cli.templates.builders import add_to_storage
from cli.templates.builders.controller import BuildController
from cli.templates.storage import JSXComponentExtras
from cli.templates.ui.content import text_content
from cli.templates.ui.mappings.storage import ParentMappings
from cli.templates.utils import compress, compress_imports, str_to_list

from zentra.core import Component
from zentra.core.html import Div
from zentra.core.react import LucideIcon

from zentra.nextjs import Link, NextJs
from zentra.ui.control import Button, ToggleGroup
from zentra.ui.notification import Tooltip


class ParentComponentBuilder:
    """A builder for creating Zentra `Component` model JSX for components that have other components inside of them."""

    def __init__(
        self,
        component: Component,
        mappings: ParentMappings,
        details_dict: dict[str, ComponentDetails],
    ) -> None:
        self.component = component
        self.maps = mappings
        self.details = details_dict

        self.controller = BuildController(
            mappings=mappings.controller,
            details_dict=details_dict,
        )
        self.storage = JSXComponentExtras()

    def build(self, model: Component = None) -> list[str]:
        """Builds the JSX for the component and returns the content as a list of strings."""
        if model is None:
            model = self.component

        shell, storage = self.controller.build_component(model, full_shell=True)
        self.storage = add_to_storage(self.storage, storage)

        # TODO: refactor to remove need for attributes + specific models
        # Need better DRY code!
        if hasattr(model, "content"):
            builder = InnerContentBuilder(
                component=model,
                controller=self.controller,
                storage=self.storage,
            )
            inner_content, storage = builder.build()
            self.storage = add_to_storage(self.storage, storage, extend=True)

        elif hasattr(model, "items"):
            items: list[Component] = model.items
            inner_content = []
            for item in items:
                inner_content.extend(self.build(model=item))

            if isinstance(model, ToggleGroup):
                inner_content, self.storage = self.handle_toggle_group(
                    inner_content,
                    self.storage,
                )

        if isinstance(model, Tooltip):
            return self.handle_tooltip_content(model, shell)
        # Refactor end

        self.storage.imports = compress_imports(self.storage.imports)
        return [shell[0], *inner_content, *shell[1:]]

    def handle_toggle_group(
        self,
        content: list[str],
        storage: JSXComponentExtras,
    ) -> tuple[list[str], JSXComponentExtras]:
        """Updates the `Toggle` item names in the `ToggleGroup` content to `ToggleGroupItem` and removes `Toggle` from the storage imports. Returns the updated information as a tuple in the form of: `(content, storage)`."""
        updated_content = []
        t_start, t_end = "<Toggle", "</Toggle"
        tg_start, tg_end = "<ToggleGroupItem", "</ToggleGroupItem"

        for item in content:
            if item.startswith(t_start):
                updated_content.append(item.replace(t_start, tg_start))
            elif item.startswith(t_end):
                updated_content.append(item.replace(t_end, tg_end))
            else:
                updated_content.append(item)

        toggle_import = [item for item in storage.imports if '/ui/toggle"' in item][0]
        storage.imports.remove(toggle_import)
        return updated_content, storage

    def handle_tooltip_content(self, model: Tooltip, shell: list[str]) -> list[str]:
        """Updates the `Tooltip` component content by wrapping the `Tooltip` in a `TooltipProvider` and adds the trigger component content into the `TooltipTrigger`. Returns the updated content list."""
        trigger_open = shell[:2]
        trigger_close = shell[2:]

        if model.trigger.classname in self.maps.parent:
            trigger_content = self.build(model.trigger)
        elif isinstance(model.trigger, NextJs):
            trigger_content, storage = self.controller.build_nextjs_component(
                model.trigger
            )
            self.storage = add_to_storage(self.storage, storage)
        else:
            trigger_content, storage = self.controller.build_component(model.trigger)
            self.storage = add_to_storage(self.storage, storage)

        return [
            "<TooltipProvider>",
            *trigger_open,
            *trigger_content,
            *trigger_close,
            "</TooltipProvider>",
        ]


class InnerContentBuilder:
    """A builder for creating the inner JSX for Zentra models with the 'content' attribute."""

    def __init__(
        self,
        component: Component,
        controller: BuildController,
        storage: JSXComponentExtras,
    ) -> None:
        self.component = component
        self.controller = controller
        self.storage = storage

        self.content: Div | str | LucideIcon | Component = self.component.content

    def build(self) -> tuple[list[str], JSXComponentExtras]:
        """Builds the JSX and returns it as a tuple in the form: `(content, multi_comp_storage)`."""
        if isinstance(self.content, Div):
            inner_content = self.build_div_content(self.content)

        elif isinstance(self.component, Button):
            inner_content, storage = self.build_btn_content(self.component)
            self.storage = add_to_storage(self.storage, storage, extend=True)

        elif isinstance(self.content, str):
            inner_content: list[str] = text_content(self.content)

        elif isinstance(self.content, LucideIcon):
            inner_content, import_str = self.controller.build_icon(self.content)
            self.storage.imports.append(import_str)

        else:
            if isinstance(self.content, NextJs):
                inner_content, storage = self.controller.build_nextjs_component(
                    self.content
                )
            else:
                inner_content, storage = self.controller.build_component(self.content)

            storage.imports = str_to_list(storage.imports)
            self.storage = add_to_storage(self.storage, storage, extend=True)

        return inner_content, self.storage

    def build_div_content(self, content: Div) -> list[str]:
        """Builds the `Div` content of the model and returns it as a list of strings."""
        content, comp_storage = self.controller.build_html_tag(model=content)
        self.storage = add_to_storage(self.storage, comp_storage, extend=True)
        return content

    def build_btn_content(self, model: Button) -> tuple[list[str], JSXComponentExtras]:
        """Creates the JSX for a `Button` models inner content and returns its details as a tuple in the form of `(content, multi_comp_storage)`."""
        storage = JSXComponentExtras()

        if isinstance(model.content, LucideIcon):
            model.content, import_str = self.controller.build_icon(model.content)
            storage.imports.append(import_str)
        else:
            model.content = text_content(model.content)

        if model.url:
            model.content = compress(model.content)
            model.content, link_storage = self.controller.build_nextjs_component(
                Link(href=model.url, text=model.content)
            )
            storage = add_to_storage(storage, link_storage)

        return model.content, storage

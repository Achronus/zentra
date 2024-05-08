from cli.conf.storage import ComponentDetails
from cli.templates.builders import add_to_storage
from cli.templates.builders.utils import get_html_content
from cli.templates.builders.jsx import (
    AttributeBuilder,
    ContentBuilder,
    ImportBuilder,
    LogicBuilder,
)
from cli.templates.mappings import JSXMappings
from cli.templates.storage import JSXComponentContentStorage, JSXComponentExtras
from cli.templates.ui.content import text_content
from cli.templates.utils import compress, compress_imports, str_to_list

from zentra.core import Component
from zentra.core.base import HTMLTag, JSIterable
from zentra.core.html import Div, FigCaption, Figure, HTMLContent
from zentra.core.react import LucideIcon, LucideIconWithText

from zentra.nextjs import Link, NextJs
from zentra.ui.control import Button, ToggleGroup
from zentra.ui.notification import Tooltip


class BuildController:
    """A controller for selecting Zentra model JSX builders."""

    def __init__(
        self, mappings: JSXMappings, details_dict: dict[str, ComponentDetails]
    ) -> None:
        self.maps = mappings
        self.details_dict = details_dict

    def build_component(
        self, component: Component, full_shell: bool = False
    ) -> tuple[list[str], JSXComponentContentStorage]:
        """Creates the JSX for a `Component` model and returns its details as a tuple in the form of `(content, comp_storage)`."""
        builder = ComponentBuilder(
            component=component,
            mappings=self.maps,
            details=self.details_dict[component.classname],
        )
        builder.build(full_shell=full_shell)
        return str_to_list(builder.storage.content), builder.storage

    def build_nextjs_component(
        self, component: Component
    ) -> tuple[list[str], JSXComponentContentStorage]:
        """Creates the JSX for a `NextJS` model and returns its details as a tuple in the form of `(content, comp_storage)`."""
        nextjs = NextJSComponentBuilder(component=component, mappings=self.maps)
        nextjs.build()
        return str_to_list(nextjs.storage.content), nextjs.storage

    def build_js_iterable(
        self, model: JSIterable
    ) -> tuple[list[str], JSXComponentExtras]:
        """Creates the JSX for a `JSIterable` model and returns its details as a tuple in the form of `(content, multi_comp_storage)`."""
        builder = JSIterableContentBuilder(
            model=model,
            mappings=self.maps,
            details_dict=self.details_dict,
        )
        content = builder.build()
        return content, builder.comp_storage

    def build_html_tag(self, model: HTMLTag) -> tuple[list[str], JSXComponentExtras]:
        """Creates the JSX for a `HTMLTag` model and returns its details as a tuple in the form of `(content, multi_comp_storage)`."""
        builder = HTMLBuildController(
            model=model,
            mappings=self.maps,
            details_dict=self.details_dict,
        )
        content, storage = builder.build()
        return content, storage

    def build_icon(self, model: LucideIcon) -> tuple[list[str], str]:
        """Creates the JSX for a `LucideIcon` model and returns its details as a tuple in the form of: `(content, import_str)`."""
        builder = IconBuilder(model=model, mappings=self.maps)
        content, import_str = builder.build()
        return content, import_str


class HTMLBuildController:
    """A build controller for creating Zentra `HTMLTag` models as JSX."""

    def __init__(
        self,
        model: HTMLTag,
        mappings: JSXMappings,
        details_dict: dict[str, ComponentDetails],
    ) -> None:
        self.model = model
        self.maps = mappings
        self.details_dict = details_dict

        self.storage = JSXComponentExtras()

    def build(self) -> tuple[list[str], JSXComponentExtras]:
        """Builds the models JSX content and returns it as a tuple in the form: `(content, storage)`"""

        if isinstance(self.model, Div):
            builder = DivBuilder(
                model=self.model,
                mappings=self.maps,
                details_dict=self.details_dict,
            )
        elif isinstance(self.model, HTMLContent):
            builder = HTMLContentBuilder(self.model, self.maps)

        elif isinstance(self.model, Figure):
            builder = FigureBuilder(
                model=self.model,
                mappings=self.maps,
                details_dict=self.details_dict,
            )
        else:
            raise TypeError(f"'{type(self.model)}' not supported.")

        content, storage = builder.build()
        self.storage = add_to_storage(self.storage, storage, extend=True)
        return content, self.storage


class ParentComponentBuilder:
    """A builder for creating Zentra `Component` model JSX for components that have other components inside of them."""

    def __init__(
        self,
        component: Component,
        mappings: JSXMappings,
        details_dict: dict[str, ComponentDetails],
    ) -> None:
        self.component = component
        self.mappings = mappings
        self.details = details_dict

        self.controller = BuildController(
            mappings=mappings,
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

        if model.trigger.classname in self.mappings.parent_components:
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


class IconBuilder:
    """A builder for creating the JSX for `LucideIcon` Zentra models."""

    def __init__(
        self, model: LucideIcon | LucideIconWithText, mappings: JSXMappings
    ) -> None:
        self.model = model
        self.maps = mappings

        self.attrs = AttributeBuilder(
            component=model,
            common_mapping=mappings.common_attrs,
            component_mapping=mappings.component_attrs,
        )

    def build(self) -> tuple[list[str], str]:
        """Creates the JSX for the model and return its details as a tuple in the form of: `(content, import_str)`."""
        content = self.create_container()

        if isinstance(self.model, LucideIconWithText):
            content = self.handle_text(content)

        return content, self.model.import_str

    def handle_text(self, content: list[str]) -> list[str]:
        """Manages the text location and preprocessing inside the `content` list. Returns the updated list."""
        if self.model.text:
            self.model.text = text_content(self.model.text)[0]
            if self.model.position == "start":
                content.append(self.model.text)
            else:
                content.insert(0, self.model.text)

        return content

    def create_container(self) -> list[str]:
        """Creates the icon container and applies the attributes to it. Returns it as a list of strings."""
        attrs_str = compress(self.attrs.build(), chars=" ")
        return [
            f'<{self.model.name} className="mr-2 h-4 w-4"{f' {attrs_str}' if attrs_str else ''} />'
        ]


class NextJSComponentBuilder:
    """A builder for creating Zentra `NextJS` models as JSX."""

    def __init__(self, component: Component, mappings: JSXMappings) -> None:
        self.component = component
        self.wrapper_map = mappings.wrappers

        self.storage = JSXComponentContentStorage()
        self.attrs = AttributeBuilder(
            component=component,
            common_mapping=mappings.common_attrs,
            component_mapping=mappings.component_attrs,
        )
        self.import_builder = ImportBuilder(
            component=component,
            additional_imports_mapping=mappings.additional_imports,
            use_state_mapping=mappings.use_state_map,
            core_name=component.container_name,
            child_names=[],
        )
        self.content = ContentBuilder(
            model=component,
            model_mapping=mappings.component_content,
            common_mapping=mappings.common_content,
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


class JSIterableContentBuilder:
    """A builder for creating Zentra `JSIterable` model content as JSX."""

    def __init__(
        self,
        model: JSIterable,
        mappings: JSXMappings,
        details_dict: dict[str, ComponentDetails],
    ) -> None:
        self.model = model
        self.maps = mappings
        self.details_dict = details_dict

        self.controller = BuildController(
            mappings=mappings,
            details_dict=details_dict,
        )
        self.comp_storage = JSXComponentExtras()

    def build(self) -> list[str]:
        """Builds the content for the JSX iterable and returns it as a list of strings. If the the content inside is a component, also stores its information in `self.storage`."""
        start, end = self.get_container()
        inner_model: HTMLTag | Component = self.model.content

        if isinstance(inner_model, HTMLTag):
            content, storage = self.controller.build_html_tag(inner_model)
            self.comp_storage = add_to_storage(self.comp_storage, storage, extend=True)

        elif isinstance(inner_model, NextJs):
            content, storage = self.controller.build_nextjs_component(inner_model)
            self.comp_storage = add_to_storage(self.comp_storage, storage)

        else:
            try:
                content, storage = self.controller.build_component(inner_model)
                self.comp_storage = add_to_storage(self.comp_storage, storage)
            except AttributeError:
                raise AttributeError(
                    f"'JSIterableContentBuilder.build(details=None)'. Missing 'ComponentDetails' for provided '{inner_model.classname}' Component",
                )

        return [start, *content, end]

    def get_container(self) -> tuple[str, str]:
        """Creates the outer shell of the iterable and returns it in the form of `(start, end)`."""
        start = (
            "{"
            + f"{self.model.obj_name}.{self.model.classname}(({self.model.param_name}) => ("
        )
        end = "))}"
        return start, end


class ComponentBuilder:
    """A builder for creating Zentra `Component` models as JSX."""

    def __init__(
        self, component: Component, mappings: JSXMappings, details: ComponentDetails
    ) -> None:
        self.component = component
        self.details = details
        self.maps = mappings

        self.storage = JSXComponentContentStorage()
        self.attrs = AttributeBuilder(
            component=component,
            common_mapping=mappings.common_attrs,
            component_mapping=mappings.component_attrs,
        )
        self.imports = ImportBuilder(
            component=component,
            additional_imports_mapping=mappings.additional_imports,
            use_state_mapping=mappings.use_state_map,
            core_name=details.name,
            child_names=details.child_names,
        )
        self.logic = LogicBuilder(
            component=component,
            logic_mapping=mappings.common_logic,
        )
        self.content = ContentBuilder(
            model=component,
            model_mapping=mappings.component_content,
            common_mapping=mappings.common_content,
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

        if self.component.classname in self.maps.wrappers.keys():
            wrapped_content = [
                f"<div {self.maps.wrappers[self.component.classname]}>",
                *wrapped_content,
                "</div>",
            ]

        return wrapped_content


class DivBuilder:
    """A builder for creating the `Div` Zentra HTML model content as JSX."""

    def __init__(
        self,
        model: Div,
        mappings: JSXMappings,
        details_dict: dict[str, ComponentDetails],
    ) -> None:
        self.model = model
        self.maps = mappings
        self.details_dict = details_dict

        self.controller = BuildController(mappings=mappings, details_dict=details_dict)

        self.storage = JSXComponentExtras()
        self.inner_content = []

    def build(self) -> tuple[list[str], JSXComponentExtras]:
        """Builds the JSX content and returns it as a tuple in the form: `(content, storage)`."""
        if not isinstance(self.model.items, list):
            self.model.items = [self.model.items]

        shell_start, shell_end = get_html_content(self.model, self.maps)
        self.build_content(self.model.items)
        content = [shell_start, *self.inner_content, shell_end]

        return content, self.storage

    def build_content(
        self,
        item: str
        | Component
        | JSIterable
        | list[str | HTMLTag | Component | JSIterable],
    ) -> None:
        """Builds the content for the `Div` model and stores the content in `self.inner_content` and any component information in `self.storage`."""
        if isinstance(item, JSIterable):
            content, storage = self.controller.build_js_iterable(item)
            self.inner_content.extend(content)
            self.storage = add_to_storage(self.storage, storage, extend=True)

        elif isinstance(item, Component):
            content, storage = self.controller.build_component(item)
            self.inner_content.extend(content)
            self.storage = add_to_storage(self.storage, storage)

        elif isinstance(item, Figure):
            builder = FigureBuilder(
                model=item,
                mappings=self.maps,
                details_dict=self.details_dict,
            )
            content, storage = builder.build()
            self.inner_content.extend(content)
            self.storage = add_to_storage(self.storage, storage, extend=True)

        elif isinstance(item, HTMLContent):
            content, _ = HTMLContentBuilder(model=item, mappings=self.maps).build()
            self.inner_content.extend(content)

        elif isinstance(item, Div):
            shell_start, shell_end = get_html_content(item, self.maps)
            self.inner_content.append(shell_start)
            self.build_content(item.items)
            self.inner_content.append(shell_end)

        elif isinstance(item, str):
            self.inner_content.extend(text_content(item))

        elif isinstance(item, list):
            for i in item:
                self.build_content(item=i)

        else:
            raise TypeError(f"'{type(item)}' not supported.")


class HTMLContentBuilder:
    """A builder for creating the `HTMLContent` Zentra HTML model content as JSX."""

    def __init__(self, model: HTMLContent, mappings: JSXMappings) -> None:
        self.model = model
        self.maps = mappings

        self.storage = JSXComponentExtras()

    def build(self) -> tuple[list[str], JSXComponentExtras]:
        """Builds the JSX content and returns it as a tuple in the form: `(content, storage)`."""
        content = get_html_content(model=self.model, mappings=self.maps)
        return content, self.storage


class FigureBuilder:
    """A builder for creating the `Figure` Zentra HTML model content as JSX."""

    def __init__(
        self,
        model: Figure,
        mappings: JSXMappings,
        details_dict: dict[str, ComponentDetails],
    ) -> None:
        self.model = model
        self.maps = mappings
        self.details_dict = details_dict

        self.controller = BuildController(mappings=mappings, details_dict=details_dict)

        self.storage = JSXComponentExtras()

    def build(self) -> tuple[list[str], JSXComponentExtras]:
        """Builds the JSX content and returns it as a tuple in the form: `(content, storage)`."""
        content = []
        shell_start, shell_end = get_html_content(model=self.model, mappings=self.maps)

        fig_content = FigCaptionBuilder(
            model=self.model.caption,
            mappings=self.maps,
        ).build()
        img_content, nextjs_storage = self.controller.build_nextjs_component(
            component=self.model.img
        )
        self.storage = add_to_storage(self.storage, nextjs_storage)

        if self.model.img_container_styles:
            img_content.insert(0, f'<div className="{self.model.img_container_styles}"')
            img_content.append("</div>")

        content.extend(img_content)
        content.extend(fig_content)

        content.insert(0, shell_start)
        content.append(shell_end)

        return content, self.storage


class FigCaptionBuilder:
    """A builder for creating the `FigCaption` Zentra HTML model content as JSX."""

    def __init__(self, model: FigCaption, mappings: JSXMappings) -> None:
        self.model = model
        self.maps = mappings

    def build(self) -> list[str]:
        """Builds the JSX content and returns it as a list of strings."""
        if not isinstance(self.model.text, list):
            self.model.text = [self.model.text]

        inner_content = []
        for item in self.model.text:
            if isinstance(item, HTMLTag):
                inner_content.extend(get_html_content(model=item, mappings=self.maps))
            elif isinstance(item, str):
                inner_content.append(text_content(item)[0])

        self.model.text = inner_content
        return get_html_content(self.model, self.maps)

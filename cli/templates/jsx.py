import re
from typing import Callable

from cli.conf.format import name_from_camel_case
from cli.conf.storage import ComponentDetails
from cli.templates.mappings import JSXMappings
from cli.templates.ui.content import text_content
from cli.templates.utils import (
    compress_imports,
    dedupe,
    compress,
    remove_none,
    str_to_list,
)
from cli.templates.storage import (
    JSXComponentContentStorage,
    JSXComponentExtras,
    JSXPageContentStorage,
)

from zentra.core import Component, Page
from zentra.core.base import HTMLTag, JSIterable
from zentra.core.html import Div, FigCaption, Figure
from zentra.core.react import LucideIcon
from zentra.nextjs import Link, NextJs
from zentra.ui import Form
from zentra.ui.control import Button, InputOTP, ToggleGroup
from zentra.ui.notification import Tooltip


FORM_SCHEMA_BASE = """
const FormSchema = z.object({
  **form_schema**
});
"""

JSX_BASE = """**imports**

type Props = {
  **props**
}
**form_schema**
const PageName = (**prop_params**: Props) => {
  **logic**
  return (
      **content**
  );
};

export default PageName;
"""


def add_to_storage(
    local: JSXComponentExtras,
    comp_store: JSXComponentContentStorage | JSXComponentExtras,
    extend: bool = False,
) -> JSXComponentExtras:
    """A helper function for adding component items to storage. Returns the updated storage."""
    for key in local.__dict__.keys():
        if hasattr(comp_store, key):
            value = getattr(comp_store, key)
            if value:
                local_values: list[str] = getattr(local, key)
                local_values.extend(value) if extend else local_values.append(value)

    local.imports = dedupe(local.imports)
    local.logic = dedupe(local.logic)
    return local


class JSXPageBuilder:
    """A builder for creating Zentra `Page` models as JSX."""

    def __init__(
        self,
        page: Page,
        mappings: JSXMappings,
        component_details: list[ComponentDetails],
    ) -> None:
        self.page = page
        self.mappings = mappings
        self.component_details = component_details

        self.storage = JSXPageContentStorage()
        self.use_client = False
        self.form_schema_base = FORM_SCHEMA_BASE
        self.jsx = JSX_BASE

    def get_details(self, component: Component) -> ComponentDetails:
        """Retrieves the component details for the component."""
        for details in self.component_details:
            if component.classname == details.name:
                return details

    def build(self) -> None:
        """Builds the JSX for the page."""

        for component in self.page.components:
            self.check_for_use_client(component=component)
            details = self.get_details(component=component)
            builder = ComponentBuilder(
                component=component,
                mappings=self.mappings,
                details=details,
            )
            builder.build()
            self.populate_storage(comp_store=builder.storage)

        self.fill_jsx()

        if self.use_client:
            self.jsx = f'"use_client"\n\n{self.jsx}'

    def check_for_use_client(self, component: Component) -> None:
        """Performs a check to enable `use_client` at the top of the page if any required components exist."""
        if component.classname in self.mappings.use_client_map:
            self.use_client = True

    def populate_storage(self, comp_store: JSXComponentContentStorage) -> None:
        """Adds component items to storage."""
        for key in self.storage.__dict__.keys():
            if hasattr(comp_store, key):
                getattr(self.storage, key).append(getattr(comp_store, key))

    def fill_jsx(self) -> None:
        """Concatenates the lists of JSX content into strings, removes duplicate imports and redundant logic statements, and adds them to the appropriate areas in the JSX template."""
        imports = self.set_imports(self.storage.imports)
        logic = self.set_logic(self.storage.logic)
        content = self.set_content(self.storage.content)
        form_schema = self.set_form_schema(self.storage.form_schema)
        props, prop_params = self.set_props(self.storage.props)

        self.jsx = self.jsx.replace("PageName", self.page.name)
        self.jsx = self.jsx.replace("**imports**", imports)
        self.jsx = self.jsx.replace("**logic**", logic)
        self.jsx = self.jsx.replace("**content**", content)
        self.jsx = self.jsx.replace("**form_schema**", form_schema)
        self.jsx = self.jsx.replace("**props**", props)
        self.jsx = self.jsx.replace("**prop_params**", prop_params)

    def unpack_additional_imports(self, imports_list: list[str]) -> list[str]:
        """Unpacks additional import values if a newline character is present in the list."""
        unpacked_imports = []
        for import_str in imports_list:
            if "\n" in import_str:
                unpacked_imports.extend(import_str.split("\n"))
            else:
                unpacked_imports.append(import_str)
        return unpacked_imports

    def compress_lucide_react(self, imports: list[str]) -> list[str]:
        """Combines `lucide-react` imports into a single statement (if applicable). Returns the updated/unedited list."""
        seen_lucide, new_imports = [], []
        lucide_base = 'import { **parts** } from "lucide-react"'

        for statement in imports:
            if "lucide-react" in statement:
                icon = statement.split(" ")[2]
                if icon not in seen_lucide:
                    seen_lucide.append(icon)
            else:
                new_imports.append(statement)

        if len(seen_lucide) > 0:
            parts = ", ".join(seen_lucide)
            lucide_base = lucide_base.replace("**parts**", parts)
            new_imports.append(lucide_base)
            return new_imports

        return imports

    def group_imports(self, imports: list[str]) -> list[str]:
        """Splits import statements into groups for better readability. Returns an updated import list."""
        non_components, components = [], []

        for statement in imports:
            if "@/components" not in statement:
                non_components.append(statement)
            else:
                components.append(statement)

        if len(non_components) > 0:
            non_components.append("")
            return non_components + components

        return imports

    def compress(self, values: list[str]) -> str:
        """Compresses values into a string."""
        return "\n".join(values)

    def dedupe(self, values: list[str]) -> list[str]:
        """Filters out duplicate values from the list."""
        result = list(set(values))
        result.sort()
        return result

    def set_form_schema(self, form_schema: list[str]) -> str:
        """Sets the form schema depending on if a form exists in the page. If one does, uses `form_schema_base` to populate the values and returns it. Otherwise, returns an empty string."""
        if form_schema:
            form_schema = self.compress(self.storage.form_schema)
            return self.form_schema_base.replace("**form_schema**", form_schema)
        else:
            return ""

    def set_imports(self, imports: list[str]) -> str:
        """Sets the import statements depending on the values stored in storage and returns them as a compiled string."""
        imports = self.unpack_additional_imports(imports)
        imports = self.compress_lucide_react(imports)
        imports = self.group_imports(self.dedupe(imports))
        return self.compress(imports)

    def set_logic(self, logic: list[str]) -> str:
        """Sets the page logic depending on the values stored in storage and returns them as a compiled string."""
        return self.compress(logic).strip("\n")

    def set_content(self, content: list[str]) -> str:
        """Sets the page JSX content depending on the values stored in storage and returns them as a compiled string."""
        content.insert(0, "<>")
        content.append("</>")
        return self.compress(content)

    def set_props(self, props: list[str]) -> tuple[str, str]:
        """Sets the prop content and prop parameters depending on the values stored in storage and returns them as a compiled string."""
        if props:
            # TODO: update logic here
            return self.compress(props), self.compress(props)
        else:
            return "", "props"


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
        builder = HTMLContentBuilder(
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
        if isinstance(comp_storage, JSXComponentContentStorage):
            self.storage = add_to_storage(self.storage, comp_storage)
        elif isinstance(comp_storage, JSXComponentExtras):
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

    def __init__(self, model: LucideIcon, mappings: JSXMappings) -> None:
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

        if hasattr(self.model, "text"):
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
            mappings=mappings,
            child_names=[],
        )
        self.content = ContentBuilder(component=component, mappings=mappings)

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
        name = self.component.classname
        return f"import {name} from 'next/{name.lower()}'"

    def apply_content_containers(self, content: list[str]) -> list[str]:
        """Wraps the components content in its outer shell and any additional wrappers (if applicable)."""
        wrapped_content = [
            f"<{self.component.classname}{f' {self.storage.attributes}' if self.storage.attributes else ''} />"
        ]

        if len(content) > 0:
            wrapped_content[0] = wrapped_content[0].replace(" />", ">")
            wrapped_content.extend(
                [
                    *content,
                    f"</{self.component.classname}>",
                ]
            )

        if self.component.classname in self.wrapper_map.keys():
            wrapped_content = [
                f"<div {self.wrapper_map[self.component.classname]}>",
                *wrapped_content,
                "</div>",
            ]

        return wrapped_content


class HTMLContentBuilder:
    """A builder for creating Zentra `HTML` model content as JSX."""

    def __init__(
        self,
        model: HTMLTag,
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
        self.inner_content = []

    def build(self, model: HTMLTag = None) -> tuple[list[str], JSXComponentExtras]:
        """Builds a single item's content and returns it as a list of strings."""
        if model is None:
            model = self.model

        if hasattr(model, "text"):
            self.handle_text(text=model.text)
            model.text = self.inner_content

        if isinstance(model, Div):
            self.build_div_model(item=model.items)
            model.items = self.inner_content

        if isinstance(model, Figure):
            content = self.build_figure_model(model=model)
            return content, self.comp_storage

        return self.get_content(model=model), self.comp_storage

    def build_figure_model(self, model: Figure) -> list[str]:
        """Builds the content for the Figure model, stores any component information in `self.comp_storage` and returns the Figure's contents as a list of strings."""
        content = []
        shell_start, shell_end = self.get_content(model=model)

        img_content, nextjs_storage = self.controller.build_nextjs_component(model.img)
        self.comp_storage = add_to_storage(self.comp_storage, nextjs_storage)

        content.append(shell_start)

        if model.img_container_styles:
            img_content.insert(0, f'<div className="{model.img_container_styles}"')
            img_content.append("</div>")

        fig_content = self.build_fig_caption(model=model.caption)
        content.extend(img_content)
        content.extend(fig_content)
        content.append(shell_end)

        self.inner_content.extend(content)
        return content

    def build_fig_caption(self, model: FigCaption) -> list[str]:
        """Builds the content for the `FigCaption` model and and returns it as a list of strings."""
        start_idx_caption_content = len(self.inner_content)
        self.handle_text(model.text)

        caption_content = self.inner_content[start_idx_caption_content:]
        current_content = self.inner_content[:start_idx_caption_content]

        self.inner_content = current_content
        model.text = caption_content

        return self.get_content(model=model)

    def build_div_model(
        self,
        item: str
        | Component
        | JSIterable
        | list[str | HTMLTag | Component | JSIterable],
    ) -> None:
        """Builds the content for the `Div` model and stores the content in `self.inner_content` and any component information in `self.comp_storage`."""
        if isinstance(item, JSIterable):
            content, storage = self.controller.build_js_iterable(item)
            self.inner_content.extend(content)
            self.comp_storage = add_to_storage(self.comp_storage, storage, extend=True)

        elif isinstance(item, Component):
            content, storage = self.controller.build_component(item)
            self.inner_content.extend(content)
            self.comp_storage = add_to_storage(self.comp_storage, storage)

        elif isinstance(item, Figure):
            self.inner_content.extend(self.build_figure_model(model=item))

        elif isinstance(item, HTMLTag):
            self.inner_content.extend(self.get_content(model=item))

        elif isinstance(item, str):
            self.handle_text(text=item)

        elif isinstance(item, list):
            for i in item:
                self.build_div_model(item=i)

    def handle_text(self, text: str | HTMLTag | list[str | HTMLTag]) -> None:
        """Handles the content building for the text attribute and stores it in `self.inner_content`."""
        if isinstance(text, list):
            for item in text:
                self.handle_text(text=item)

        if isinstance(text, HTMLTag):
            self.inner_content.extend(self.get_content(model=text))
        elif isinstance(text, str):
            self.inner_content.append(text_content(text)[0])

    def get_content(self, model: HTMLTag) -> list[str]:
        """A helper function to build the content of the HTMLTag and returns it as a list of strings."""
        attr_builder = AttributeBuilder(
            component=model,
            common_mapping=self.maps.common_attrs,
            component_mapping=self.maps.component_attrs,
        )
        content_builder = ContentBuilder(component=model, mappings=self.maps)

        attributes = " ".join(attr_builder.build())
        content = content_builder.build()
        return self.html_content_container(
            model=model, content=content, attributes=attributes
        )

    def html_content_container(
        self, model: HTMLTag, content: list[str], attributes: list[str]
    ) -> list[str]:
        """Performs content container wrapping for HTMLTags."""
        wrapped_content = [
            f"<{model.classname}{f" {attributes}" if attributes else ''}>"
        ]

        if len(content) > 0:
            wrapped_content.extend(content)

        wrapped_content.append(f"</{model.classname}>")

        if isinstance(model, Div):
            if model.shell:
                wrapped_content[0] = "<>"
                wrapped_content[-1] = "</>"

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
        model: HTMLTag | Component = self.model.content

        if isinstance(model, HTMLTag):
            content, storage = self.controller.build_html_tag(model)
            self.comp_storage = add_to_storage(self.comp_storage, storage, extend=True)

        elif isinstance(model, NextJs):
            content, storage = self.controller.build_nextjs_component(model)
            self.comp_storage = add_to_storage(self.comp_storage, storage)

        else:
            try:
                content, storage = self.controller.build_component(model)
                self.comp_storage = add_to_storage(self.comp_storage, storage)
            except AttributeError:
                raise AttributeError(
                    f"'JSIterableContentBuilder.build(details=None)'. Missing 'ComponentDetails' for provided '{model.classname}' Component",
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
            mappings=mappings,
            child_names=details.child_names,
        )
        self.logic = LogicBuilder(component=component, mappings=mappings)
        self.content = ContentBuilder(component=component, mappings=mappings)

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
            f"<{self.component.classname}{f' {self.storage.attributes}' if self.storage.attributes else ''} />"
        ]

        if len(content) > 0 or full_shell:
            wrapped_content[0] = wrapped_content[0].replace(" />", ">")
            wrapped_content.extend(
                [
                    *content,
                    f"</{self.component.classname}>",
                ]
            )

        if self.component.classname in self.maps.wrappers.keys():
            wrapped_content = [
                f"<div {self.maps.wrappers[self.component.classname]}>",
                *wrapped_content,
                "</div>",
            ]

        return wrapped_content


class FormBuilder:
    """A builder for creating Zentra `Form` models as JSX."""

    def __init__(self, form: Form) -> None:
        self.form = form

    def build(self) -> str:
        """Builds the JSX for the form."""
        for field in self.form:
            # TODO: access sub-components
            # field.content
            pass


class AttributeBuilder:
    """
    A builder for creating Zentra `Component` attributes.

    Parameters:
    - `component` (`zentra.core.Component`) - any Zentra Component model
    - `common_mapping` (`dictionary[string, callable]`) - a mapping containing common attributes across all components. With a `{key: value}` pair = `{attr_name, attr_func}`
    - `component_mapping` (`dictionary[string, callable]`) - a mapping containing unique component specific logic. With a `{key: value}` pair = `{component_name: attr_func}`.
    """

    def __init__(
        self,
        component: Component,
        common_mapping: dict[str, Callable],
        component_mapping: dict[str, Callable],
    ) -> None:
        self.component = component
        self.common_map = common_mapping
        self.component_map = component_mapping

    def get_common_attr(self, key: str, value: int | str | bool) -> str:
        """Retrieves an attribute string from the common attribute mapping given a key, value pair."""
        return self.common_map[key](value)

    def get_component_attrs(self) -> list[str]:
        """Retrieves a list of unique attribute strings for the component from the component attribute mapping."""
        return self.component_map[self.component.classname](self.component)

    def common_checks(self, attr_name: str) -> bool:
        """Performs checks for model attributes to confirm whether it should use the `common_map`. These include:
          1. When the `attr_name` is not an `inner_attribute`
          2. When the `attr_name` is not a `custom_common_attribute`

        If both checks are valid, returns `True`. Otherwise, returns `False`.
        """
        not_inner_attr = attr_name not in self.component.inner_attributes
        not_custom_attr = attr_name not in self.component.custom_common_attributes

        if not_inner_attr and not_custom_attr:
            return True

        return False

    def build(self) -> list[str]:
        """Builds the attributes from a mapping for the component."""
        attrs = []
        include_common = True
        model_dict = self.component.__dict__

        for attr_name, value in model_dict.items():
            if value is not None:
                if isinstance(self.component, (Component, LucideIcon)):
                    include_common = self.common_checks(attr_name)

                if attr_name in self.common_map.keys() and include_common:
                    attr_str = self.get_common_attr(attr_name, value)
                    attrs.append(attr_str)

        if (
            isinstance(self.component, Component)
            and self.component.classname in self.component_map.keys()
        ):
            attr_list = self.get_component_attrs()

            if attr_list is not None:
                attrs.extend(attr_list)

        return remove_none(attrs)


class ImportBuilder:
    """A builder for creating Zentra `Component` import statements."""

    def __init__(
        self, component: Component, mappings: JSXMappings, child_names: list[str]
    ) -> None:
        self.component = component
        self.additional_map = mappings.additional_imports
        self.use_state_map = mappings.use_state_map
        self.child_names = child_names

    def build(self) -> list[str]:
        """Builds the import statements for the component."""
        additional_imports = self.additional_imports()
        use_state = self.use_state()
        imports = [self.core_import()]

        if use_state:
            imports.extend(use_state)

        if additional_imports:
            imports.extend(additional_imports)

        return [item for item in imports if item]

    def core_import(self) -> str:
        """Creates the core import statement for the component."""
        filename = name_from_camel_case(self.component.classname)
        return f'import {{ {self.core_import_pieces()} }} from "@/components/{self.component.library}/{filename}"'.replace(
            "'", " "
        )

    def get_imports_from_map(self) -> str:
        """A helper function to retrieve the additional imports from the `additional_map` for the component."""
        return self.additional_map[self.component.classname](self.component)

    def additional_imports(self) -> list[str]:
        """Creates the additional imports needed for the component."""
        imports = []

        if (
            isinstance(self.component, Component)
            and self.component.classname in self.additional_map.keys()
        ):
            attr_list = self.get_imports_from_map()

            if attr_list is not None:
                imports.extend(attr_list)

        if len(imports) == 0:
            return None

        return imports

    def core_import_pieces(self) -> str:
        """Creates the core import pieces including the main component and its children (if required)."""
        return ", ".join([self.component.classname] + self.child_names)

    def use_state(self) -> list[str]:
        """Adds React's `useState` import if the component requires it."""
        if self.component.classname in self.use_state_map:
            return ['import { useState } from "react"']
        return None


class ContentBuilder:
    """A builder for creating Zentra `Component` content."""

    def __init__(self, component: Component, mappings: JSXMappings) -> None:
        self.component = component
        self.maps = mappings

    def build(self) -> list[str]:
        """Builds the content for the component."""
        content = []

        for attr_name, condition in self.maps.common_content:
            if isinstance(self.component, InputOTP):
                content.extend(self.handle_input_otp())

            elif hasattr(self.component, attr_name):
                value = getattr(self.component, attr_name)
                if value:
                    content_str = condition(value)
                    content.append(content_str)

                    if attr_name == "text" and isinstance(self.component, Tooltip):
                        content.pop()

        for comp_type, condition in self.maps.component_content:
            if isinstance(self.component, comp_type):
                content_str = condition(self.component)
                if content_str:
                    content.extend(content_str)

        if len(content) > 0 and isinstance(content[0], list):
            return self.handle_single_quotes(*content)

        return self.handle_single_quotes(content)

    def handle_input_otp(self) -> list[str]:
        """Input OTP is difficult to create with a single list comprehension. Instead, we create it separately here."""
        content = []
        component: InputOTP = self.component

        slot_group_size = component.num_inputs // component.num_groups
        slot_idx = 0

        group_tag = "InputOTPGroup>"

        for group_idx in range(component.num_groups):
            content.append(f"<{group_tag}")
            for _ in range(slot_group_size):
                content.append(f"<InputOTPSlot index={{{slot_idx}}} />")
                slot_idx += 1
            content.append(f"</{group_tag}")

            if component.num_groups > 1 and group_idx + 1 != component.num_groups:
                content.append("<InputOTPSeparator />")

        return content

    def handle_single_quotes(self, content: list[str]) -> list[str]:
        """Checks for `'` in a content list. If the item is a string without JSX tags, it will update the text into a suitable format for JSX processing. Returns the updated content list or unmodified version."""
        single_quote_pattern = re.compile(r"\b\w*'\w*\b")

        for idx, line in enumerate(content):
            sq_matches = single_quote_pattern.findall(line)

            if sq_matches:
                for match in sq_matches:
                    wrapped = "{`" + match + "`}"
                    content[idx] = re.sub(
                        r"\b" + re.escape(match) + r"\b", wrapped, line
                    )

        return content


class LogicBuilder:
    """A builder for creating the Zentra `Component` function logic created above the `return` statement."""

    def __init__(self, component: Component, mappings: JSXMappings) -> None:
        self.component = component
        self.maps = mappings

    def build(self) -> list[str]:
        """Builds the function logic for the component."""
        logic = []

        for item in self.maps.common_logic:
            comp_type, attr_name, condition = item
            if isinstance(self.component, comp_type):
                value = getattr(self.component, attr_name)
                if value:
                    logic.extend(condition(value))

        return logic

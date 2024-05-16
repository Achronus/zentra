from zentra.core import Component
from zentra.core.enums.ui import SeparatorVariant
from zentra.core.utils import name_to_pascal_case
from zentra.custom import CustomModel


class SeparatorModel(Component, CustomModel):
    """
    A custom helper Zentra model that acts as a drop in replacement for unique `Separator` child components in the [Shadcn/ui](https://ui.shadcn.com/) component library, such as `BreadcrumbSeparator` or `DropdownMenuSeparator`.

    Dynmaically assigns the JSX content in the `content_str` property based on a given `variant` and set of `styles`. Not intended to be used solo. Applied to specific `zentra.ui` models, such as `DDMSeparator` and content methods like `dropdown_menu_content()`. Refer to `variant` parameter for more details.

    Parameters:
    - `variant` (`string`) - defines the type of separator to create. Valid options: `['breadcrumb', 'dropdown_menu', 'menubar', 'command', 'context_menu']`. Each option applies a different name to the separator which are required in other components. Here are the options:
      1. `breadcrumb` -> `BreadcrumbSeparator`
      2. `dropdown_menu` -> `DropdownMenuSeparator`
      3. `menubar` -> `MenubarSeparator`
      4. `command` -> `CommandSeparator`
      5. `context_menu` -> `ContextMenuSeparator`
    - `styles` (`string, optional`) - an optional set of CSS classes. `None` by default
    """

    variant: SeparatorVariant
    styles: str = None

    @property
    def container_name(self) -> str:
        return f"{name_to_pascal_case(self.variant)}Separator"

    @property
    def content_str(self) -> str:
        """Defines the JSX content for the component."""
        content = f'<{self.container_name}{f' className="{self.styles}"' if self.styles else ''} />'

        if self.variant == "breadcrumb":
            content += '\n<span className="sr-only">Toggle menu</span>'

        return content

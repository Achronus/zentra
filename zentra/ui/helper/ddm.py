from zentra.core import Component

from zentra.core.utils import compress, str_to_list
from zentra.ui import ShadcnUi
from zentra.ui.helper.utils import full_container, param_attr, str_attr


class DDMRadioGroup(Component, ShadcnUi):
    """
    A helper model that handles the content creation for the `DropdownMenuRadioGroup` component in the [Shadcn/ui](https://ui.shadcn.com/docs/components/dropdown-menu#radio-group) component library.

    Parameters:
    - `items` (`list[string]`) - a list of strings for the content of each radio group item
    - `value` (`string, optional`) - the name for the `hook` value. Automatically added to `value` as a parameter. `ddrgPosition` by default
    - `on_change` (`string, optional`) - the name for the `set` value. Automatically added to `onValueChange` as a parameter. `ddrgSetPosition` by default
    """

    items: list[str]
    value: str = "ddPosition"
    on_change: str = "ddSetPosition"

    @property
    def container_name(self) -> str:
        return "DropdownMenuRadioGroup"

    def process_value(self, item: str) -> str:
        """A helper function for formatting the content of the `value` prop dynamically."""
        if len(item.split(" ")) >= 2:
            item = item.split(" ")[:2]
            item = compress(item, chars="-")

        return item.lower()

    def content(self) -> list[str]:
        """Creates the JSX content for the child component."""
        content = []
        for item in self.items:
            item_attrs = str_attr("value", self.process_value(item))
            content.append(
                full_container("DropdownMenuRadioItem", item, attrs=item_attrs)
            )

        group_attrs = compress(
            [
                param_attr("value", self.value),
                param_attr("onValueChange", self.on_change),
            ],
            chars=" ",
        )
        return str_to_list(
            full_container(self.container_name, content, attrs=group_attrs)
        )

    def logic(self) -> list[str]:
        """Creates the logic for the child component."""
        init_val = self.process_value(self.items[0])
        return [f'const [{self.value}, {self.on_change}] = useState("{init_val}");']


class DDMCheckboxGroup(Component, ShadcnUi):
    """
    A helper model that handles the content creation for a set of `DropdownMenuCheckboxItem` components in the [Shadcn/ui](https://ui.shadcn.com/docs/components/dropdown-menu#checkboxes) component library.

    Parameters:
    - `items` (`list[string]`) - a list of strings for the content of each radio group item
    """

    items: list[str]

    @property
    def get_name(self) -> str:
        return "show"

    @property
    def set_name(self) -> str:
        return "setShow"

    def process_value(self, item: str) -> str:
        """A helper function for formatting the content of the `value` prop dynamically."""
        if len(item.split(" ")) >= 2:
            item = item.split(" ")[:2]
            return compress([i.capitalize() for i in item], chars="")

        return item.capitalize()

    def content(self) -> list[str]:
        """Creates the JSX content for the child component."""
        content = []
        for item in self.items:
            item_attrs = compress(
                [
                    param_attr("checked", f"{self.get_name}{self.process_value(item)}"),
                    param_attr(
                        "onCheckedChange", f"{self.set_name}{self.process_value(item)}"
                    ),
                ],
                chars=" ",
            )
            content.extend(
                str_to_list(
                    full_container("DropdownMenuCheckboxItem", item, attrs=item_attrs)
                )
            )

        return content

    def logic(self) -> list[str]:
        """Creates the logic for the child component."""

        def handle_item(item: str, state_val: str = "false") -> str:
            name = self.process_value(item)
            return f"const [{self.get_name}{name}, {self.set_name}{name}] = useState({state_val});"

        logic = [handle_item(self.items[0], "true")]
        for item in self.items[1:]:
            logic.append(handle_item(item))

        return logic

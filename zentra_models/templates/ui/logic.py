from zentra_models.core.enums.ui import CalendarMode
from zentra_models.ui.control import Calendar, Collapsible, Combobox, Pagination
from zentra_models.ui.presentation import Progress


def hook_simple(
    get_name: str,
    set_name: str,
    value: str,
    value_type: str = None,
    hook_name: str = "State",
) -> str:
    """A helper function for creating simple hook statements such as `useState(false)`."""
    value_type = f"<{value_type}>" if value_type else ""

    return f"const [{get_name}, {set_name}] = use{hook_name}{value_type}({value});"


def hook_use_effect(
    content: str, cleanup: str = None, dependencies: list[str] = None
) -> str:
    """A helper function for creating the `useEffect` hook."""
    deps = ", ".join(dependencies) if dependencies else ""

    output = [
        "useEffect(() => {\n",
        content,
        "\n}, " + f"[{deps}])",
    ]

    if cleanup:
        last = output.pop()
        output.extend(["\nreturn () => {\n", cleanup, "\n};", last])

    return "".join(output)


def calendar_logic(comp: Calendar) -> list[str]:
    """Returns a list of strings for the `Calendar` logic based on the given name value."""

    if comp.mode == CalendarMode.SINGLE.value:
        return [
            hook_simple(
                comp.use_state_names[0],
                comp.use_state_names[1],
                value="new Date()",
                value_type="Date | undefined",
            ),
        ]
    elif comp.mode == CalendarMode.MULTIPLE.value:
        return [
            "const initiallySelectedDates = [new Date(), addDays(new Date(), 1)];",
            hook_simple(
                comp.use_state_names[0],
                comp.use_state_names[1],
                value="[]",
                value_type="Date[]",
            ),
        ]
    else:
        return [
            hook_simple(
                comp.use_state_names[0],
                comp.use_state_names[1],
                value="{ from: new Date(), to: addDays(new Date(), 4)}",
                value_type="DateRange | undefined",
            ),
        ]


def collapsible_logic(comp: Collapsible) -> list[str]:
    """Returns a list of strings for the `Collapsible` logic based on the given name value."""
    return [hook_simple(f"{comp.name}IsOpen", f"{comp.name}SetIsOpen", value="false")]


def pagination_logic(comp: Pagination) -> list[str]:
    """Returns a list of strings for the `Pagination` logic based on the given name value."""
    return [
        f"const itemsPerPage = {comp.items_per_page};",
        f"const maxItems = {comp.total_items};",
        hook_simple(comp.start_idx_name[0], comp.start_idx_name[1], value="0"),
        hook_simple(comp.end_idx_name[0], comp.end_idx_name[1], value="itemsPerPage"),
    ]


def progress_logic(prog: Progress) -> list[str]:
    """Returns a list of strings for the `Progress` logic based on the given name value."""
    return [
        hook_simple(prog.use_state_names[0], prog.use_state_names[1], value=prog.min),
        hook_use_effect(
            f"const timer = setTimeout(() => {prog.use_state_names[1]}({prog.value}), {prog.max});",
            cleanup="clearTimeout(timer);",
        ),
    ]


def combobox_logic(box: Combobox) -> list[str]:
    """Returns a list of strings for the `Combobox` logic based on the given name value."""
    return [
        hook_simple(*box.open_state_names, value="false"),
        hook_simple(*box.value_state_names, value='""'),
    ]

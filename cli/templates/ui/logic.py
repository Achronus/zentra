from zentra.ui.control import Calendar, Collapsible, Pagination
from zentra.ui.navigation import DDMCheckboxGroup, DropdownMenu, DDMRadioGroup
from zentra.ui.presentation import Progress


def hook_assignment(get_name: str, set_name: str) -> str:
    """A helper function for creating the assignment portion a hook statement."""
    return f"const [{get_name}, {set_name}] ="


def calendar_logic(comp: Calendar) -> list[str]:
    """Returns a list of strings for the `Calendar` logic based on the given name value."""
    assignment = hook_assignment(f"{comp.name}Date", f"{comp.name}SetDate")
    return [f"{assignment} useState<Date | undefined>(new Date());"]


def collapsible_logic(comp: Collapsible) -> list[str]:
    """Returns a list of strings for the `Collapsible` logic based on the given name value."""
    assignment = hook_assignment(f"{comp.name}IsOpen", f"{comp.name}SetIsOpen")
    return [f"{assignment} useState(false);"]


def pagination_logic(comp: Pagination) -> list[str]:
    """Returns a list of strings for the `Pagination` logic based on the given name value."""
    start_idx = hook_assignment(comp.start_idx_name[0], comp.start_idx_name[1])
    end_idx = hook_assignment(comp.end_idx_name[0], comp.end_idx_name[1])
    return [
        f"const itemsPerPage = {comp.items_per_page};",
        f"const maxItems = {comp.total_items};",
        f"{start_idx} useState(0);",
        f"{end_idx} useState(itemsPerPage);",
    ]


def dropdown_menu_logic(dd: DropdownMenu) -> list[str]:
    """Returns a list of strings for the `DropdownMenu` logic based on the given name value."""

    def radio_group(rg: DDMRadioGroup) -> list[str]:
        logic = []

        for idx, text in enumerate(rg.texts):
            get_name, set_name = rg.state_name_pairs[idx]
            hook = hook_assignment(get_name, set_name)
            hook_value = rg.values[0] if rg.values else text.split(" ")[0].lower()
            logic.append(f'{hook} useState("{hook_value}")')

        return logic

    def checkbox_group(cbg: DDMCheckboxGroup) -> list[str]:
        logic = []

        for idx, _ in enumerate(cbg.texts):
            get_name, set_name = cbg.state_name_pairs[idx]
            hook = hook_assignment(get_name, set_name)
            state_val = "true" if idx == 0 else "false"
            logic.append(f"{hook} useState<Checked>({state_val});")

        return logic

    if isinstance(dd.items, DDMRadioGroup):
        return radio_group(dd.items)
    elif isinstance(dd.items, DDMCheckboxGroup):
        return checkbox_group(dd.items)

    return []


def progress_logic(prog: Progress) -> list[str]:
    """Returns a list of strings for the `Progress` logic based on the given name value."""
    return [
        f"{hook_assignment(prog.use_state_names[0], prog.use_state_names[1])} useState({prog.min});",
        "useEffect(() =< {",
        f"const timer = setTimeout(() => setProgress({prog.value}), {prog.max});",
        "return () => clearTimeout(timer);",
        "}, [])",
    ]

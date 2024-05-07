from zentra.ui.control import Calendar, Collapsible


def hook_assignment(get_name: str, set_name: str) -> str:
    """A helper function for creating the assignment portion a hook statement."""
    return f"const [{get_name}, {set_name}] ="


def calendar_logic(comp: Calendar) -> list[str]:
    """Returns a list of strings for the Calendar logic based on the given name value."""
    assignment = hook_assignment(f"{comp.name}Date", f"{comp.name}SetDate")
    return [f"{assignment} useState<Date | undefined>(new Date());"]


def collapsible_logic(comp: Collapsible) -> list[str]:
    """Returns a list of strings for the Collapsible logic based on the given name value."""
    assignment = hook_assignment(f"{comp.name}IsOpen", f"{comp.name}SetIsOpen")
    return [f"{assignment} useState(false);"]

def calendar_logic(name: str) -> list[str]:
    """Returns a list of strings for the Calendar logic based on the given name value."""
    return [
        f"const [{name}Date, {name}SetDate] = useState<Date | undefined>(new Date());"
    ]


def collapsible_logic(name: str) -> list[str]:
    """Returns a list of strings for the Collapsible logic based on the given name value."""
    return [f"const [{name}IsOpen, {name}SetIsOpen] = useState(false);"]

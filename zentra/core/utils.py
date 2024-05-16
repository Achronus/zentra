def name_to_pascal_case(name: str) -> str:
    """
    Converts a name from lowercase underscored format to pascal case.

    Example:
    - dropdown_menu -> DropdownMenu
    """
    components = name.split("_")
    return "".join(item.title() for item in components)

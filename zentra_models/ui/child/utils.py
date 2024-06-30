from zentra_models.core.constants import PARAMETER_PREFIX
from zentra_models.core.utils import compress


def simple_container(name: str, attrs: str = None) -> str:
    """A helper function for creating a self closing component."""
    return f"<{name}{f' {attrs}' if attrs else ''} />"


def full_container(name: str, content: str | list[str], attrs: str = None) -> str:
    """A helper function to create a component with a full container. Applies the `name` and `attrs` to the start wrapper. Returns the updated content as a `string`."""
    start = f"<{name}{f' {attrs}' if attrs else ''}>"
    end = f"</{name}>"

    if isinstance(content, str):
        return compress([start, content, end])

    return compress([start, *content, end])


def str_attr(name: str, value: str) -> str:
    """A helper function for creating string attribute strings, such as `color="red"`."""
    return f'{name}="{value}"'


def param_attr(name: str, value: int | str | bool, backticks: bool = False) -> str:
    """A helper function for creating parameter attribute strings, such as `size={48}`, `checked={false}`, or ```alt={`I have a {param} here`}```."""
    if isinstance(value, bool):
        value = str(value).lower()
    elif isinstance(value, str) and value.startswith(PARAMETER_PREFIX):
        value = value[len(PARAMETER_PREFIX) :]

    if backticks:
        return f"{name}={{`{value}`}}"

    return f"{name}={{{value}}}"

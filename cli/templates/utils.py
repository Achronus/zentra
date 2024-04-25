def compress(values: list[str], chars: str = "\n") -> str:
    """Compresses values into a string."""
    return chars.join(values)


def dedupe(values: list[str]) -> list[str]:
    """Filters out duplicate values from the list."""
    result = list(set(values))
    result.sort()
    return result


def str_to_list(content: str, sep: str = "\n") -> list[str]:
    """Converts a string into a list of strings based on a given separator."""
    return content.split(sep=sep)

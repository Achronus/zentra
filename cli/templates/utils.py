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


def remove_none(values: list[str]) -> list[str]:
    """sanitize the `None` values from a list of strings and returns the new list."""
    return [item for item in values if item]


def compress_imports(imports: list[str]) -> list[str]:
    """Merges imports with the same `from` into a single import. Returns the updated import list."""
    imports_dict: dict[str, list[str]] = {}

    for item in imports:
        module = item.split(" ")[-1]
        comps = item.replace("import", "").strip().split("from")[0].strip(" {}")

        comp_list = [item.strip() for item in comps.split(",")]

        if module in imports_dict.keys():
            imports_dict[module].extend(comp_list)
        else:
            imports_dict[module] = comp_list

    merged_imports = []
    for module, comps in imports_dict.items():
        comps = list(set(comps))
        comps.sort()

        if "next/" not in module:
            comps = "{ " + ", ".join(comps) + " }"
        else:
            comps = comps[0]

        merged_imports.append(f"import {comps} from {module}")

    return merged_imports

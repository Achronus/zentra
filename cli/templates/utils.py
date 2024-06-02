import re

from zentra.core.constants import PARAMETER_PREFIX


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

    def check_extensions(module: str) -> list[bool]:
        remote_item = []
        for extension in ["next/", ".jpg", ".png", ".webp"]:
            if extension not in module:
                remote_item.append(True)
            else:
                remote_item.append(False)

        return remote_item

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

        remote_item = all(check_extensions(module))
        if remote_item:
            comps = "{ " + ", ".join(comps) + " }"
        else:
            comps = comps[0]

        if "use client" not in comps:
            merged_imports.append(f"import {comps} from {module}")

    return merged_imports


def handle_single_quotes(content: list[str]) -> list[str]:
    """Checks for `'` in a content list. If the item is a string without JSX tags, it will update the text into a suitable format for JSX processing. Returns the updated content list or unmodified version."""
    single_quote_pattern = re.compile(r"\b\w*'\w*\b")

    for idx, line in enumerate(content):
        sq_matches = single_quote_pattern.findall(line)

        if sq_matches:
            for match in sq_matches:
                wrapped = "{`" + match + "`}"
                content[idx] = re.sub(r"\b" + re.escape(match) + r"\b", wrapped, line)

    return content


def text_content(text: str) -> str:
    """Returns a list of strings of text content with variable preprocessing."""
    new_text = []
    for word in text.split(" "):
        if word:
            if word.startswith(PARAMETER_PREFIX):
                new_text.append(f"{{{word[len(PARAMETER_PREFIX):]}}}")
            else:
                new_text.append(word)

    new_text = handle_single_quotes(new_text)
    return " ".join(new_text)

import re


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


def param_reformat_helper(text: str) -> list[str]:
    """A helper function to reformat a string of text with parameter values. Returns the new version as a list of strings."""
    new_text = []
    for word in text.split(" "):
        if word:
            if word.startswith("$"):
                new_text.append(f"{{{word[1:]}}}")
            else:
                new_text.append(word)

    new_text = handle_single_quotes(new_text)
    return [" ".join(new_text)]


def text_content(text: str | list[str]) -> list[str]:
    """Returns a list of strings of text content with variable preprocessing
    (if required)."""
    if isinstance(text, str):
        return param_reformat_helper(text)

    return text

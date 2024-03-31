import os
from cli.conf.storage import ComponentDetails
from cli.conf.types import FolderFilePair


def extract_component_details(
    component_pairs: FolderFilePair, root_dir: str, sub_dir: str
) -> list[ComponentDetails]:
    """Retrieves a list of component information for the provided (folder, filename) pairs from the root component directory and a provided sub-directory.Stores them in a `ComponentDetails` object."""
    all_components = []
    seen_files = set()

    def extract_components(file_content: str) -> list[str]:
        start_idx = file_content.find("export {") + len("export {")
        end_idx = file_content.find("}", start_idx)
        if start_idx != -1 and end_idx != -1:
            components = (
                file_content[start_idx:end_idx].replace(" ", "").replace("\n", "")
            )
        return components.lstrip("{").rstrip(",").split(",")

    def filter_components(components: list[str]) -> str:
        filtered = [
            item
            for item in components
            if not item.endswith("Variants")
            and not item.startswith("type")
            and not item.endswith("Style")
            and not item.startswith("use")
        ]

        return filtered

    def set_components(file_content: str) -> list[str]:
        components = extract_components(file_content)
        return filter_components(components)

    if os.path.exists(root_dir):
        search_files = [
            os.path.join(root_dir, folder, sub_dir, filename)
            for folder, filename in component_pairs
        ]

        for filepath in search_files:
            if ".tsx" in filepath:
                filename = os.path.basename(filepath)
                file_tuple = (component_pairs[0], filename)

                if file_tuple not in seen_files:
                    with open(filepath, "r") as f:
                        file_content = f.read()

                    components = set_components(file_content)
                    component = ComponentDetails(
                        library=component_pairs[0],
                        filename=filename,
                        component_name=components[0],
                        child_component_names=components[1:],
                    )

                    all_components.append(component)
                    seen_files.add(file_tuple)
    else:
        raise FileNotFoundError(f"'{root_dir}' does not exist.")

    return all_components

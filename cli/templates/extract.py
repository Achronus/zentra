import os
from cli.conf.extract import get_filename_dir_pairs
from cli.conf.storage import BasicNameStorage, ComponentDetails, CountStorage
from cli.conf.types import LibraryNamePairs
from cli.templates.retrieval import ComponentStorage


class ModelExtractor:
    """
    Handles the functionality for extracting models from GitHub and preparing them
    for file generation.

    Parameters:
    - `url` (`string`) - the GitHub URL housing the component files
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self.filenames: ComponentStorage = None

    def component_base_names(self) -> LibraryNamePairs:
        """Returns a list of `(library_name, filename)` pairs extracted from `ComponentStorage`."""
        base_names = []
        for lib_name, values in self.filenames.__dict__.items():
            for filename in values.base:
                base_names.append((lib_name, filename))

        return base_names

    def folders(self) -> list[str]:
        """Returns a list of `library_name` folders."""
        return [lib_name for lib_name in self.filenames.__dict__.keys()]


class LocalExtractor:
    """
    Handles the functionality for extracting information from `zentra/models`.

    Parameters:
    - `generate_path` (`string`) - the path to the Zentra generate folder
    - `name_storage` (`storage.BasicNameStorage`) - the Zentra application name storage containing the user model filenames
    """

    def __init__(self, generate_path: str, name_storage: BasicNameStorage) -> None:
        self.generate_path = generate_path
        self.name_storage = name_storage

        self.model_counts = CountStorage()

    def find_difference(
        self, pair_one: LibraryNamePairs, pair_two: LibraryNamePairs
    ) -> LibraryNamePairs:
        """Identifies the differences between two lists of pairs of Zentra models."""
        same = list(set(pair_one) & set(pair_two))
        return list(set(pair_one + pair_two) - set(same))

    def user_models(self) -> list[str]:
        """Retrieves the Zentra model filenames from `zentra/models`."""
        return self.name_storage.filenames

    def existing_models(self) -> LibraryNamePairs:
        """Retrieves the existing Zentra model filenames from the Zentra generate folder."""
        return get_filename_dir_pairs(parent_dir=self.generate_path)

    def format_user_models(
        self, pairs: LibraryNamePairs, targets: list[str]
    ) -> LibraryNamePairs:
        """
        Reformats the user defined Zentra models into a list of `(library_name, filename)` pairs.

        Parameters:
        - `pairs` (`FolderFilePair`) - a list of all `(library_name, filename)` component pairs
        - `targets` (`list[str]`) - a list of file or folder names to extract from the file list. Can be a single item.
        """
        return [item for item in pairs if item[1] in targets]

    def model_changes(
        self, existing: LibraryNamePairs, user_model_pairs: LibraryNamePairs
    ) -> tuple[LibraryNamePairs, LibraryNamePairs]:
        """Provides two lists of `FolderFilePair` changes. In the form of: `(to_remove, to_add)`."""
        to_remove, to_add = [], []
        existing_models_set = set(existing)

        model_updates = self.find_difference(existing, user_model_pairs)
        for model in model_updates:
            if model in existing_models_set:
                to_remove.append(model)
                self.model_counts.remove += 1
            else:
                to_add.append(model)
                self.model_counts.generate += 1

        return to_remove, to_add


def extract_component_details(
    component_pairs: LibraryNamePairs, root_dir: str, sub_dir: str
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

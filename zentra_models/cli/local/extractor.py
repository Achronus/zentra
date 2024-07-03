import typer

from zentra_models.cli.constants import GenerateSuccessCodes
from zentra_models.cli.constants.filepaths import GENERATE_PATHS
from zentra_models.cli.local.files import get_filename_dir_pairs
from zentra_models.cli.local.storage import BasicNameStorage, CountStorage
from zentra_models.cli.constants.types import LibraryNamePairs


class LocalExtractor:
    """
    Handles the functionality for extracting information from `zentra/models`.

    Parameters:
    - `name_storage` (`storage.BasicNameStorage`) - the Zentra application name storage containing the user model filenames
    """

    def __init__(self, name_storage: BasicNameStorage) -> None:
        self.name_storage = name_storage

        self.model_counts = CountStorage()

    def find_difference(
        self, pair_one: LibraryNamePairs, pair_two: LibraryNamePairs
    ) -> LibraryNamePairs:
        """Identifies the differences between two lists of pairs of Zentra models."""
        same = list(set(pair_one) & set(pair_two))
        return list(set(pair_one + pair_two) - set(same))

    def user_models(self) -> LibraryNamePairs:
        """Retrieves the Zentra model filenames from `zentra/models`."""
        return self.name_storage.filenames

    def existing_models(self) -> LibraryNamePairs:
        """Retrieves the existing Zentra model filenames from the Zentra generate folder."""
        return get_filename_dir_pairs(GENERATE_PATHS.ROOT)

    def model_changes(
        self, existing: LibraryNamePairs, user_models: LibraryNamePairs
    ) -> tuple[LibraryNamePairs, LibraryNamePairs]:
        """Provides two lists of `FolderFilePair` changes. In the form of: `(to_add, to_remove)`."""
        to_remove, to_add = [], []
        existing_models_set = set(existing)

        model_updates = self.find_difference(existing, user_models)
        for model in model_updates:
            if model in existing_models_set:
                to_remove.append(model)
                self.model_counts.remove += 1
            else:
                to_add.append(model)
                self.model_counts.generate += 1

        return to_add, to_remove

    @staticmethod
    def no_new_components_check(
        user_models: LibraryNamePairs, existing: LibraryNamePairs
    ) -> None:
        """Raises an error if there are no new components to create."""
        if user_models == existing:
            raise typer.Exit(code=GenerateSuccessCodes.NO_NEW_COMPONENTS)

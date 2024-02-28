import os


class FileHandler:
    """A class dedicated to managing files."""

    def __init__(self, folder_path: str) -> None:
        self.folder_path = folder_path

    def make_path_dirs(self) -> None:
        """Creates the directories for `self.folder_path` if they don't already exist."""
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

    def check_folder_exists(self) -> bool:
        """Checks if the `self.folder_path` exists in the current working directory."""
        if os.path.exists(self.folder_path) and os.path.isdir(self.folder_path):
            return True

        return False

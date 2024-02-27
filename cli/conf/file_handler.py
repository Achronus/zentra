import os


class FileHandler:
    def __init__(self, folder_path: str) -> None:
        self.folder_path = folder_path

    def check_folder_exists(self) -> bool:
        """Checks if the `self.folder_path` exists in the current working directory."""
        if os.path.exists(self.folder_path) and os.path.isdir(self.folder_path):
            return True

        return False

    def check_folder_empty(self) -> bool:
        """Checks if the `self.folder_path` contains any files."""
        if self.check_folder_exists() and len(os.listdir(self.folder_path)) == 0:
            return True

        return False

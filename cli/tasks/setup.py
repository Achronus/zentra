import os

from ..conf.file_handler import FileHandler


class Setup:
    def __init__(self) -> None:
        self.folder_name = "zentra"
        self.folder_path = os.path.join(os.getcwd(), self.folder_name)

        self.fh = FileHandler(self.folder_path)

        self.zentra_exists = self.fh.check_folder_exists()
        self.zentra_empty = self.fh.check_folder_empty()

import ast
import os


class FileHandler:
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

    def check_folder_empty(self) -> bool:
        """Checks if the `self.folder_path` contains any files."""
        if self.check_folder_exists() and len(os.listdir(self.folder_path)) == 0:
            return True

        return False

    def get_python_files(self) -> list[str]:
        """Retrieves a list of python files in the `self.folder_path`, if any exist."""
        return [file for file in os.listdir(self.folder_path) if file.endswith(".py")]

    def check_component_model_exists(self) -> bool:
        """Checks if a `Component` model exists in any of the python files in `self.folder_path`."""
        valid_files = self.get_python_files()

        for file in valid_files:
            filepath = os.path.join(self.folder_path, file)

            with open(filepath, "r") as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for base in node.bases:
                        if isinstance(base, ast.Name) and base.id == "Component":
                            return True

        return False

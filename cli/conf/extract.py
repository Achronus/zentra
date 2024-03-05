import os


def get_filenames_in_subdir(filepath: str) -> list[str]:
    """Retrieves a list of all filenames in a `filepath`. Ignores folder subdirectories."""
    filenames = []
    for root, dirs, files in os.walk(filepath):
        for file in files:
            if file.endswith("py"):
                filenames.append(os.path.join(root, file))
    return filenames

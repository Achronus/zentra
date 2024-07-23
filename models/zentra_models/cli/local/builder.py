import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from zentra_models.core.utils import name_from_pascal_case


class FilepathBuilder(BaseModel):
    """
    A model for creating filepaths associated to Zentra models.

    Parameters:
    - `name` (`string`) - name in PascalCase
    - `library` (`string`) - the name of the component library
    - `local_root` (`Path`) - the filepath to the local directory
    - `package_root` (`Path`) - the filepath to the Zentra models directory
    - `ext` (`string, optional`) - the filepath extension. `tsx` by default
    - `local_sub` (`string, optional`) - the name of the sub-directory found between the `(library, filename)` in the local directory. `None` by default
    - `package_sub` (`string, optional`) - the name of the sub-directory found between the `(library, filename)` in the package directory. `None` by default
    """

    name: str
    library: str
    local_root: Path
    package_root: Path
    ext: Optional[str] = "tsx"
    local_sub: str = ""
    package_sub: str = ""

    def filename(self) -> str:
        """Returns the filename."""
        return f"{name_from_pascal_case(self.name)}.{self.ext}"

    def __path(self, root_path: Path, sub_dir: str) -> Path:
        """A helper method for creating the filepath."""
        return os.path.join(
            root_path,
            Path(self.library, sub_dir, self.filename()),
        )

    def local_path(self) -> Path:
        """Returns the complete local path."""
        return self.__path(self.local_root, self.local_sub)

    def package_path(self) -> Path:
        """Returns the complete package path."""
        return self.__path(self.package_root, self.package_sub)

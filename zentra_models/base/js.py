from pydantic import Field, field_validator

from zentra_models.base import ZentraModel
from zentra_models.base.library import JavaScript
from zentra_models.core.constants import LOWER_CAMELCASE_SINGLE_WORD
from zentra_models.core.validation import check_pattern_match


class JSIterable(ZentraModel, JavaScript):
    """
    A parent model for all JavaScript iterable functions.

    - `obj_name` (`string`) - the name of the data object array to iterate over. Must be `lowercase` or `camelCase`, a `single word`, and up to a maximum of `20` characters
    - `param_name` (`string`) - the name of the parameter to iterate over inside the map. Must be `lowercase` or `camelCase`, a `single word`, and up to a maximum of `20` characters
    """

    obj_name: str = Field(min_length=1, max_length=20)
    param_name: str = Field(min_length=1, max_length=20)

    @property
    def classname(self) -> str:
        """Stores the classname for the JSX builder."""
        return self.__class__.__name__.lower()

    @field_validator("obj_name", "param_name")
    def validate_name(cls, v: str) -> str:
        return check_pattern_match(
            LOWER_CAMELCASE_SINGLE_WORD,
            v,
            err_msg=f"'{v}'. Must be 'lowercase' or 'camelCase', a single word and a maximum of '20' characters\n",
        )

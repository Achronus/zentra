from pydantic import BaseModel, ConfigDict, PrivateAttr


class ZentraModel(BaseModel):
    """A base for all Zentra models."""

    _container_name = PrivateAttr(default=None)
    model_config = ConfigDict(use_enum_values=True)

    @property
    def classname(self) -> str:
        """Stores the classname for the JSX builder."""
        return self.__class__.__name__

    @property
    def container_name(self) -> str:
        """Stores the container name for the JSX builder."""
        return self._container_name if self._container_name else self.classname

    @property
    def child_names(self) -> list[str]:
        """Stores the component child names."""
        return []

    @property
    def composition_only(self) -> bool:
        """Signifies if a component is only made up of other components. When `False`, components have their own shell and import statement."""
        return False

    @property
    def content_attributes(self) -> list[str]:
        """Returns a list of attributes specific to the components content. Used for allocating the correct values to the builder."""
        if hasattr(self, "content"):
            return ["content"]

        return []

    @property
    def inner_attributes(self) -> list[str]:
        """Returns a list of the attributes that are used in the components sub-components."""
        return []

    @property
    def custom_common_attributes(self) -> list[str]:
        """Returns a list of the attributes that use the same name as a common attribute, but act differently with this specific component."""
        return []

    @property
    def custom_common_content(self) -> list[str]:
        """Returns a list of the content that use the same name as a common content, but act differently with this specific component."""
        return []

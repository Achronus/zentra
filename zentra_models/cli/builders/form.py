from zentra_models.cli.utils.format import jsx_formatter

from zentra_models.form import DynamicFormField, FormField


def to_dynamic(field: FormField) -> DynamicFormField:
    """Converts a Zentra `FormField` model into a `DynamicFormField` model."""
    field_dict = field.model_dump()

    # FormField -> DynamicFormField
    attr_map = {
        "field_type": "fieldType",
        "data": "data",
        "is_loading": "isLoading",
        "file_type_names": "fileTypes",
        "max_file_size": "maxMB",
        "img_dim_name": "maxImgDim",
    }

    for key, value in attr_map.items():
        if hasattr(field, key):
            field_dict[value] = getattr(field, key)

    return DynamicFormField(**field_dict)


class FormFieldBuilder:
    """A builder for creating Zentra form fields."""

    def __init__(self, field: FormField) -> None:
        self.field = to_dynamic(field)
        self.props = self.field.model_dump()

        self.unique_keys = {
            "fieldType": self.field_type,
        }
        self.variable_keys = [
            "control",
            "data",
            "isLoading",
            "fileTypes",
            "maxMB",
            "maxImgDim",
        ]

    def build(self) -> str:
        """Builds the JSX for a form field and returns it as a JSX formatted string."""
        props = []

        for key, value in self.props.items():
            if value is None:
                continue

            if key in self.unique_keys.keys():
                prop_str = self.unique_keys[key](key, value)
            elif key in self.variable_keys:
                prop_str = self.variable(key, str(value))
            else:
                prop_str = self.text(key, value)

            props.append(prop_str)

        return jsx_formatter(
            "\n".join(
                [
                    "<DynamicFormField",
                    *props,
                    "/>",
                ]
            )
        )

    def wrap_value(self, value: str, quotes: bool = False) -> str:
        """Wraps a value in parenthesis or quotes."""
        if quotes:
            return f'"{value}"'

        return "{" + value + "}"

    def assign_str(self, key: str, value: str) -> str:
        return f"{key}={value}"

    def field_type(self, key: str, value: str) -> str:
        value = self.wrap_value(f"FormFieldType.{value.upper()}")
        return self.assign_str(key, value)

    def variable(self, key: str, value: str) -> str:
        """Wraps a value in `{`parenthesis`}` before returning it as a string."""
        value = self.wrap_value(value)
        return self.assign_str(key, value)

    def text(self, key: str, value: str) -> str:
        """Wraps the value in `"`quotes`"` before returning it as a string."""
        value = self.wrap_value(value, quotes=True)
        return self.assign_str(key, value)

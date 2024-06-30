from pydantic.json_schema import GenerateJsonSchema

from zentra_models.ui import Form


class ZodSchema(GenerateJsonSchema):
    """A JSON schema for converting Zentra `Form` models to [Zod](https://zod.dev/)."""

    def generate(self, schema: Form, mode: str = "validation") -> dict:
        json_schema = super().generate(schema, mode=mode)
        formatted_schema = self.format_schema(json_schema)
        return formatted_schema

    def format_schema(self, json_schema: dict) -> dict:
        """Convert the schema into a simple format where each item is displayed as: {'propName': 'type'}."""
        formatted_schema = {}

        for name, info in json_schema.get("properties").items():
            new_name = self.to_camel_case(name)
            formatted_schema[new_name] = info.get("type")
        return formatted_schema

    @staticmethod
    def to_camel_case(name: str) -> str:
        """
        Converts an attribute `name` to camel case.

        Example:
        - `company_email` -> `companyEmail`
        """
        words = name.split("_")
        return words[0] + "".join(word.capitalize() for word in words[1:])


# ---------------
# Example Usage
# ---------------
# import json
# from pydantic import BaseModel

# class FormSchema(BaseModel):
#     name: str
#     company_email: str
#     company_phone: str
#     white_label: bool
#     address: str
#     city: str
#     zip_code: str
#     state: str
#     country: str
#     agency_logo: str

# schema = FormSchema.model_json_schema(schema_generator=ZodSchema)
# json_schema = json.dumps(schema, indent=2)
# print(json_schema)

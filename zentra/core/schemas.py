from pydantic.json_schema import GenerateJsonSchema


class ZodJsonSchema(GenerateJsonSchema):
    def generate(self, schema, mode="validation"):
        json_schema = super().generate(schema, mode=mode)
        formatted_schema = self.format_schema(json_schema)
        return formatted_schema

    @staticmethod
    def format_schema(json_schema: dict) -> dict:
        """Convert the schema into a simple format where each item is displayed as: {'propName': 'type'}."""
        formatted_schema = {}

        for name, info in json_schema.get("properties").items():
            new_name = ZodJsonSchema.to_camel_case(name)
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

# schema = FormSchema.model_json_schema(schema_generator=ZodJsonSchema)
# json_schema = json.dumps(schema, indent=2)
# print(json_schema)

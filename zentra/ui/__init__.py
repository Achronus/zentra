from itertools import accumulate
import json
from typing import Any

from zentra.core import Component
from zentra.core.enums.ui import FormFieldLayout

from pydantic import ConfigDict, ValidationInfo, field_validator


class FormField(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) FormField inside the Form component.

    Parameters:
    - `name` (`str`) - the name of the component
    - `label` (`str`) - the `FormLabel` text
    - `content` (`zentra.Component`) - the component to add to `FormControl`
    - `disabled` (`bool, optional`) - a flag for enabling the disabled value to `isLoading`. Default is `True`. When `False`, removes `disabled` from `FormField`
    - `description` (`str, optional`) - the `FormDescription` text. `FormDescription` is added underneath the `FormLabel`, where both are stored in a div above `FormControl`. When `None` `FormDescription` is removed from `FormField`. Default is `None`
    - `message` (`bool, optional`) - a flag for adding `FormMessage` under `FormControl`. Default is `True`. When `False`, removes `FormMessage` from `FormField`.

    Examples:
    1. Basic `FormField` without a description and only the core values added.
    ```python
    FormField(
        name="name",
        label="Agency Name",
        content=...
    )
    ```
    Into ->
    ```jsx
    <FormField
        disabled={isLoading}
        control={form.control}
        name="name"
        render={({ field }) => (
            <FormItem className="flex-1">
                <FormLabel>Agency Name</FormLabel>
                <FormControl>
                    ...
                </FormControl>
                <FormMessage />
            </FormItem>
        )}
    />
    ```

    2. A `FormField` with a description that isn't disabled on loading and has no message.
    ```python
    FormField(
        name="name",
        label="Agency Name",
        description="My awesome agency has just begun!",
        disabled=False,
        message=False,
        content=...
    )
    ```
    Into ->
    ```jsx
    <FormField
        control={form.control}
        name="name"
        render={({ field }) => (
            <FormItem className="flex-1">
                <div>
                    <FormLabel>Agency Name</FormLabel>
                    <FormDescription>
                        My awesome agency has just begun!
                    </FormDescription>
                </div>
                <FormControl>
                    ...
                </FormControl>
            </FormItem>
        )}
    />
    ```
    """

    label: str
    content: Component
    disabled: bool = True
    description: str = None
    message: bool = True


class Form(Component):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Form component.

    Parameters:
    - `name` (`str`) - the name of the component
    - `fields` (`list[FormField]`) - a list of `FormField` components
    - `layout` (`list[int]`) - a list of `integers` for grouping the fields into rows. Accepted `int` options: `[1, 2, 3]`. `layout` must equate to: `sum(layout) == len(fields)`. `fields` are automatically assigned to their row based on their position in the `fields` list

    Examples:
    1. A simple form with three fields, split into two rows.
    ```python
    Form(
        name="agencyForm",
        layout=[1, 2],
        fields=[
            FormField(
                name="agencyLogo",
                label="Agency Logo",
                content=FileUpload(name="agencyLogo"),
            ),
            FormField(
                name="name",
                label="Agency Name",
                content=Input(
                    name="name",
                    label="Agency Name",
                    placeholder="Your Agency Name",
                ),
            ),
            FormField(
                name="companyEmail",
                label="Agency Email",
                content=Input(
                    name="email",
                    label="Account Email",
                    placeholder="Email",
                    read_only=True,
                ),
            ),
        ],
    )
    ```
    Into ->
    ```jsx
    <Form {...form}>
        <form
            onSubmit={form.handleSubmit(handleSubmit)}
            className='space-y-4'
        >
            <FormField
                disabled={isLoading}
                control={form.control}
                name="agencyLogo"
                render={({ field }) => (
                    <FormItem>
                        <FormLabel>Agency Logo</FormLabel>
                        <FormControl>
                            <FileUpload
                                apiEndpoint='agencyLogo'
                                onChange={field.onChange}
                                value={field.value}
                            />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )}
            />
            <div className='flex md:flex-row gap-4'>
                <FormField
                    disabled={isLoading}
                    control={form.control}
                    name="name"
                    render={({ field }) => (
                        <FormItem className='flex-1'>
                            <FormLabel>Agency Name</FormLabel>
                            <FormControl>
                                <Input
                                    placeholder='Your Agency Name'
                                    {...field}
                                />
                            </FormControl>
                        </FormItem>
                    )}
                />
                <FormField
                control={form.control}
                name="companyEmail"
                render={({ field }) => (
                    <FormItem className="flex-1">
                    <FormLabel>Agency Email</FormLabel>
                    <FormControl>
                        <Input
                        readOnly
                        placeholder="Email"
                        {...field}
                        />
                    </FormControl>
                    <FormMessage />
                    </FormItem>
                )}
                />
            </div>
        </form>
    </Form>
    ```
    """

    fields: list[FormField]
    layout: list[FormFieldLayout]

    model_config = ConfigDict(use_enum_values=True)

    @field_validator("layout")
    @classmethod
    def field_layout_size_must_match(
        cls, layout: list[FormFieldLayout], info: ValidationInfo
    ) -> None:
        fields_len = len(info.data["fields"])
        if sum(layout) != fields_len:
            raise ValueError(
                f"'sum(layout) != len(fields)' -> '{sum(layout)} != {fields_len}'!\nEither:\n  1. Remove 'FormFields' from 'fields'\n  2. Or, update 'layout' to match 'len(fields)'\n\n"
            )
        return layout

    def __ts_schema(self) -> dict[str, Any]:
        """Generates a JSON schema for the Form in a TypeScript format."""
        output = self.model_dump()
        cumulative_row_sizes = list(accumulate(self.layout))

        for idx, field in enumerate(self.fields):
            content = {"component": field.content.__class__.__name__}
            content["attributes"] = field.content.model_dump()

            content["row"] = next(
                i for i, size in enumerate(cumulative_row_sizes, start=1) if idx < size
            )
            output["fields"][idx]["content"] = content

        return output

    def __zod_schema(self) -> dict[str, Any]:
        """Generates a JSON schema for the Form in a Zod format."""
        raise NotImplementedError()

    def schema(self, type: str = "typescript") -> dict[str, Any]:
        """
        Generates a JSON schema for the Form.

        Parameters:
        - `type` (`str, optional`) - the type of schema to generate. Options: `['typescript', 'zod']`. Default is `typescript`
        """
        if type == "typescript":
            return self.__ts_schema()
        elif type == "zod":
            return self.__zod_schema()
        else:
            raise ValueError(
                f"Invalid type='{type}'! Must be one of: ['typescript', 'zod']"
            )

    def json_schema(self, type: str = "typescript", indent: int = 2) -> str:
        """
        Generates an indented JSON schema for the Form.

        Parameters:
        - `type` (`str`) - the type of schema to generate. Options: `['typescript', 'zod']`
        - `indent` (`int, optional`) - the indent size (in spaces) for the schema. Default is `2`
        """
        return json.dumps(self.schema(type=type), indent=indent)


class FileUpload(Component):
    """A Zentra model for the [uploadthing](https://uploadthing.com/) FileUpload fields.

    Parameters:
    - `name` (`str`) - the name of the component
    """

import json
from typing import Any

from zentra_models.base.library import ShadcnUi
from zentra_models.core import Component
from zentra_models.core.enums.ui import FormFieldLayout

from pydantic import ConfigDict, field_validator
from pydantic_core import PydanticCustomError


class FormField(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) FormField inside the Form component.

    Parameters:
    - `name` (`str`) - the name of the `FormField`. Used for the [Zod object schema](https://zod.dev/?id=basic-usage)
    - `label` (`str`) - the `FormLabel` text
    - `content` (`zentra.models.Component`) - the component to add to `FormControl`
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

    name: str
    label: str
    content: Component
    disabled: bool = True
    description: str = None
    message: bool = True


class Form(Component, ShadcnUi):
    """
    A Zentra model for the [shadcn/ui](https://ui.shadcn.com/) Form component. Submit buttons are automatically created for each form and are not needed in the `fields` attribute.

    Parameters:
    - `name` (`str`) - the name of the `Form`
    - `fields` (`list[list[FormField] | FormField]`) - a list of `FormField`s as either individual values or inside additional `lists` (`list[FormField]`) to represent rows. Available row sizes include: `[2, 3]`
    - `btn_text` (`str, optional`) - the text displayed on the `Form` submission button. Default is `Submit`

    Examples:
    1. A simple form with three fields, split into two rows.
    ```python
    Form(
        name="agencyForm",
        fields=[
            FormField(
                name="agencyLogo",
                label="Agency Logo",
                content=FileUpload(),
            ),
            [
                FormField(
                    name="name",
                    label="Agency Name",
                    content=Input(
                        type="text",
                        placeholder="Your Agency Name",
                    ),
                ),
                FormField(
                    name="companyEmail",
                    label="Agency Email",
                    content=Input(
                        type="email",
                        placeholder="Email",
                    ),
                ),
            ],
        ]
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
            </div>
            <div className='flex md:flex-row gap-4'>
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
            <Button type="submit" disabled={isLoading}>
                {isLoading? <Loading/> : 'Submit'}
            </Button>
        </form>
    </Form>
    ```
    """

    name: str
    fields: list[FormField | list[FormField]]
    btn_text: str = "Submit"

    model_config = ConfigDict(use_enum_values=True)

    @field_validator("fields", mode="before")
    def validate_fields(
        cls, fields: list[list[FormField] | FormField]
    ) -> list[list[FormField]]:
        valid_sizes = [item.value for item in FormFieldLayout]
        for i, row in enumerate(fields):
            if isinstance(row, list) and len(row) not in valid_sizes:
                if len(row) == 1:
                    raise PydanticCustomError(
                        "single_valued_row",
                        f"idx: {i} -> Cannot have a single 'FormField' inside a row. Remove from 'list' or add another 'FormField'\n",
                        dict(idx=i, row=row, size=len(row)),
                    )
                else:
                    raise PydanticCustomError(
                        "invalid_row_size",
                        f"idx: {i} -> Row size ({len(row)}) too large, must be either: '{valid_sizes}'\n",
                        dict(idx=i, row=row, size=len(row)),
                    )

        return fields

    def zod_schema(self) -> dict[str, Any]:
        """Generates a Zod JSON schema for the Form in a Zod format."""
        raise NotImplementedError()

    def zod_json_schema(self, indent: int = 2) -> str:
        """
        Generates an indented Zod JSON schema for the Form.

        Parameters:
        - `indent` (`int, optional`) - the indent size (in spaces) for the schema. Default is `2`
        """
        return json.dumps(self.zod_schema(), indent=indent)

from pydantic import BaseModel


class JSXPageContentStorage(BaseModel):
    """
    A storage container for the pieces of a JSX Zentra `Page` model.

    Parameters:
    - `imports` (`list[string]`) - a list of strings representing import statements
    - `logic` (`list[string]`) - a list of strings representing the component function logic
    - `content` (`list[string]`) - a list of strings containing the JSX content used in the return statement
    - `props` (`list[string]`) - a list of strings representing the TypeScript props
    - `form_schema` (`list[string], optional`) - a list of strings representing the form schema, if the page contains a form. `None` by default
    """

    imports: list[str] = []
    logic: list[str] = []
    content: list[str] = []
    props: list[str] = []
    form_schema: list[str] = None


class JSXComponentExtras(BaseModel):
    """
    A storage container for extra information inside a Zentra model.

    Parameters:
    - `imports` (`list[string]`) - a list of strings representing the components import statements
    - `logic` (`list[string]`) - a list of strings representing the component function logic
    """

    imports: list[str] = []
    logic: list[str] = []


class JSXComponentContentStorage(BaseModel):
    """
    A storage container for the pieces of a JSX Zentra `Component` model.

    Parameters:
    - `imports` (`string`) - a string representing the components import statements
    - `logic` (`string`) - a string representing the component function logic
    - `attributes` (`string`) - a string representing the attributes used in the main component
    - `content` (`string`) - a string containing the JSX content used in the return statement
    """

    imports: str = ""
    logic: str = ""
    attributes: str = ""
    content: str = ""

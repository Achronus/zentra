# Installation

!!! warning

    Zentra should always be installed in a dedicated virtual environment to isolate it from the rest of your system. 

??? example "Unsure How? Here's an Example!"

    1. Create a new Python environment:
    ```cmd title=""
    python -m venv env
    ```

    2. Access it ([Python Docs [:material-arrow-right-bottom:]](https://docs.python.org/3/library/venv.html#how-venvs-work)):

        === "Windows"
            ```cmd title=""
            .\env\Scripts\activate
            ```
        
        === "Linux/MacOS"
            ```cmd title=""
            source env/bin/activate
            ```

Depending on your use case, you can install packages separately or download the full-suite in one command. Here's a quick comparsion between the options:

- __The Full Suite__ - includes the API and Models packages for the [FastAPI [:material-arrow-right-bottom:]](https://fastapi.tiangolo.com/) backend and builds the [Next.js [:material-arrow-right-bottom:]](https://nextjs.org/) frontend too.
- __API Only__ - includes the API package for building [FastAPI [:material-arrow-right-bottom:]](https://fastapi.tiangolo.com/) backends.
- __Models Only__ - includes the models package for building React components using Python.

## System Requirements

All Zentra packages require [Python 3.12+ [:material-arrow-right-bottom:]](https://www.python.org/) and [Poetry [:material-arrow-right-bottom:]](https://python-poetry.org/) for package management. It is multi-platform and aims to be accessible across Linux, macOS and Windows.

## Select a Package

<div class="grid cards" markdown>

-   :simple-dask:{ .lg .middle } __Zentra SDK__

    ---

    Install the complete suite in a flash.

    [:octicons-arrow-right-24: Install the SDK](/sdk)

</div>

<div class="grid cards" markdown>

-   :material-api:{ .lg .middle } __Zentra API__

    ---

    Only install the API package.

    [:octicons-arrow-right-24: Install the API](/api)

-   :simple-react:{ .lg .middle } __Zentra Models__

    ---

    Only install the Models package.

    [:octicons-arrow-right-24: Install the Models](/models)

</div>

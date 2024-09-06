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

- __The Full Suite__ - includes the API and Models packages for the [FastAPI [:material-arrow-right-bottom:]](https://fastapi.tiangolo.com/) backend and builds the [Next.js [:material-arrow-right-bottom:]](https://nextjs.org/) frontend too. Read more about the [frontend files](/starting/files/nextjs) here.
- __API Only__ - includes the API package for building [FastAPI [:material-arrow-right-bottom:]](https://fastapi.tiangolo.com/) backends.
- __Models Only__ - includes the models package for building React components using Python.

## System Requirements

All Zentra packages require [Python 3.12+ [:material-arrow-right-bottom:]](https://www.python.org/) and [Poetry [:material-arrow-right-bottom:]](https://python-poetry.org/) for package management. It is multi-platform and aims to be accessible across Linux, macOS and Windows.

## Option 1: The Full Suite

!!! info "Important"

    The Zentra SDK requires you to have the [Docker Engine](https://docs.docker.com/engine/install/) installed to create the frontend files. Please make sure you have Docker running first before using the package.

Install the [`zentra-sdk`](#) package with [Poetry [:material-arrow-right-bottom:]](https://python-poetry.org/) through [PIP [:material-arrow-right-bottom:]](https://pypi.org/project/zentra-sdk/):

```cmd title=""
pip install zentra-sdk poetry
```

## Option 2: API Only

Install the [`zentra-api`](#) package with [Poetry [:material-arrow-right-bottom:]](https://python-poetry.org/) through [PIP [:material-arrow-right-bottom:]](https://pypi.org/project/zentra-api/):

```cmd title=""
pip install zentra-api poetry
```

## Option 3: Models Only

!!! construction "Coming Soon"

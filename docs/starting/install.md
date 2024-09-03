# Installation

!!! warning

    Zentra should always be installed in a dedicated virtual environment to isolate it from the rest of your system. 

Depending on your use case, you can install packages separately or download the full-suite in one command. Here's a quick comparsion between the options:

- __The Full Suite__ - includes the API and Models packages for the [FastAPI [:material-arrow-right-bottom:]](https://fastapi.tiangolo.com/) backend and builds the [Next.js [:material-arrow-right-bottom:]](https://nextjs.org/) frontend too. Read more about the [frontend files](/files/frontend) here.
- __API Only__ - includes the API package for building [FastAPI [:material-arrow-right-bottom:]](https://fastapi.tiangolo.com/) backends.
- __Models Only__ - includes the models package for building React components using Python. No frameworks include.

## System Requirements

All Zentra packages require [Python 3.12+ [:material-arrow-right-bottom:]](https://www.python.org/) and [Poetry [:material-arrow-right-bottom:]](https://python-poetry.org/) for package management. It is multi-platform and aims to be accessible across Linux, macOS and Windows.

## Option 1: The Full Suite

!!! info

    The Zentra SDK requires you to have the [Docker Engine](https://docs.docker.com/engine/install/) installed to create the frontend files. Please make sure you have Docker running first before using the package.

To get started, install the `zentra_sdk` package with [Poetry [:material-arrow-right-bottom:]](https://python-poetry.org/) through [PIP [:material-arrow-right-bottom:]](https://pypi.org/project/zentra-sdk/):

```cmd title=""
pip install zentra_sdk poetry
```

Next, run the `init` command bootstrap a new project with a [FastAPI [:material-arrow-right-bottom:]](https://fastapi.tiangolo.com/) backend and [Next.js [:material-arrow-right-bottom:]](https://nextjs.org/) frontend in seconds!

```cmd title=""
zentra init
```

You'll find two new shiny directories in your project folder. It should look similar to this:

```cmd title=""
<project_name>/
├── backend/
│   ├── app/
│   │   └── ...
│   ├── .env
│   ├── alembic.ini
│   ├── pyproject.toml
│   └── ...
├── frontend/
│   ├── public/
│   │   └── ...
│   ├── src/
│   │   └── ...
│   ├── .env.local
│   ├── package.json
│   ├── tailwind.config.js
│   └── ...
└── venv/
    └── ...
```

<div class="grid cards" markdown>

-   :simple-fastapi:{ .lg .middle } __Backend Files__

    ---

    Read more about the backend files.

    [:octicons-arrow-right-24: FastAPI files](/starting/files/fastapi)

-   :simple-nextdotjs:{ .lg .middle } __Frontend Files__

    ---

    Read more about the frontend files.

    [:octicons-arrow-right-24: Next.js files](/starting/files/nextjs)

</div>

## Option 2: API Only

To get started, install the `API` package with [Poetry [:material-arrow-right-bottom:]](https://python-poetry.org/) through [PIP [:material-arrow-right-bottom:]](https://pypi.org/project/zentra-api/):

```cmd title=""
pip install zentra-api poetry
```

Then create a new project with:

```cmd title=""
zentra-api init <project_name>
```

<div class="grid cards" markdown>

-   :simple-fastapi:{ .lg .middle } __Backend Files__

    ---

    Read more about the backend files.

    [:octicons-arrow-right-24: FastAPI files](/starting/files/fastapi)

</div>


## Option 3: Models Only

!!! construction "Coming Soon"

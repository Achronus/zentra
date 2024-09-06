# Zentra SDK: The Basics

This chapter focuses on getting started with [`Zentra SDK`](#).

!!! note

    This guide assumes that you have already installed the package and have a Python virtual environment setup in your desired project folder.


## Creating a Project

Using the SDK is the easiest method for creating started with a new project.

Simply run the [`init`](#) command and you'll have a [FastAPI [:material-arrow-right-bottom:]](https://fastapi.tiangolo.com/) backend and [Next.js [:material-arrow-right-bottom:]](https://nextjs.org/) frontend in seconds! No extra parameters needed.

```cmd title=""
zentra init
```

You'll find two new shiny directories in your project folder that will look similar to this:

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

### Working With the Backend

??? question "Did you know?"

    We built the backend using the [`zentra-api`](#) package! 
    ```cmd title=""
    zentra-api init backend
    ```

    Pretty cool right?! 🤓


# Zentra API: The Basics

This chapter focuses on getting started with [`Zentra API`](#) with simple examples.

## Creating A Project

!!! tip
    
    You can skip this command if you are using [`zentra-sdk`](#)!

To create a fresh project, we use the [`init`](#) command with a custom [`<project_name>`](#) like so:

```cmd title=""
zentra-api init <project_name>
```

After a few seconds, you should see a project structure similar to the below:

```cmd title="Folder Structure"
<project_name>/
├── app/
│   ├── api/
│   │   └── ...
│   ├── auth/
│   │   └── ...
│   ├── core/
│   │   └── ...
│   └── db_models/
│       └── ...
├── migrations/
│   └── ...
├── scripts/
│   └── ...
├── tests/
│    └── ...
├── .coveragerc
├── .env
├── .gitignore
├── alembic.ini
├── pyproject.toml
├── README.md
└── zentra.root
```

<div class="grid cards" markdown>

-   :simple-fastapi:{ .lg .middle } __Backend Files__

    ---

    Read more about the backend files.

    [:octicons-arrow-right-24: FastAPI files](/starting/files/fastapi)

</div>

## Initial Setup

We need to perform a few steps to configure the backend before we can use it.

1. Firstly, enter the directory:
    ```python title=""
    cd <project_name>  # (1)!
    ```

    1. This will be [`backend`](#) if you used the [`zentra-sdk`](#)!
        ```cmd title=""
        cd backend
        ```

2. Make the project yours! Update the author details in the [`pyproject.toml`](#):
    ```toml title="backend/pyproject.toml" hl_lines="6"
    ...
    [tool.poetry]
    name = "app"
    version = "0.1.0"
    description = "A backend for processing API data."
    authors = ["Placeholder Name <placeholder@email.com>"] # (1)!
    readme = "README.md"
    ...
    ```

    1. Update me!

3. Install the poetry scripts and extra packages:
    ```cmd title=""
    poetry install
    ```

4. Test it works by running the development environment:

    ??? question "Where does this come from?"

        [`zentra-api`](#) is configured with a few helper commands using a bit of [`Poetry`](#) ✨. 
        
        This one performs the same command as:
        ```cmd title=""
        fastapi dev app/main.py --port 8080
        ```

        You can read more about the others in the [commands](/starting/commands/api) section.

    ```cmd title=""
    run-dev
    ```

5. Navigate to [http://localhost:8080/api/docs](http://localhost:8080/api/docs) and you should see your authentication routes already configured!

![FastAPI setup example](/assets/imgs/api/fastapi-auth-routes.jpg)

## Creating Routes

!!! construction "Coming Soon"

## Creating Tables

!!! construction "Coming Soon"

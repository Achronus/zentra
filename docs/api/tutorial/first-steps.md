# First Steps

Our first step is a simple one: **create a new project**. 

Zentra makes this extremely easy and provides a lot of functionality out of the box ([What's Included?](../../api/index.md#whats-included)). 

## Creating a Project

To create a new project we use the [`init`](../../api/commands/init.md) command with a custom [`<project_name>`](#) like so:

```cmd title=""
zentra-api init <project_name>
```

After a few seconds, you'll find a new project in your directory with the following file structure:

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

This may look daunting at first, but don't worry, we'll break it down for you!

## Configuration Files

!!! tip

    Already been here and know about the files? Skip to [Starting Our Project](../../api/tutorial/first-steps.md#starting-our-project) ✨

To start with, let's explore our main configuration files. You'll likely only touch these occassionally, specifically at the start of the project and towards the end when moving into production. 

Here's are configuration files:

```python title="Folder Structure" hl_lines="3-9"
<project_name>/
...
├── .coveragerc  # (1)!
├── .env  # (2)!
├── .gitignore  # (3)!
├── alembic.ini  # (4)!
├── pyproject.toml  # (5)!
├── README.md  # (6)!
└── zentra.root  # (7)!
```

1. Our [pytest [:material-arrow-right-bottom:]](https://pytest-cov.readthedocs.io/en/latest/config.html) coverage file, strictly used for testing purposes to identify the line coverage for our project. This is updated automatically and should **never** be manually edited.
2. Our environment variable file. A fundamental file to securing our sensitive information such as API keys and database details. 
    
    We recommend you get familiar with this and update any information you need to. We'll talk about this in more detail shortly.

3. A [Git [:material-arrow-right-bottom:]](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control) version control file used to ignore specific files and  directories from being pushed to platforms like GitHub. Feel free to explore this at your own leisure.
4. Our [Alembic [:material-arrow-right-bottom:]](https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file) configuration file, used for database migration tracking. We've configured this to work with new projects automatically.
5. Our [Poetry [:material-arrow-right-bottom:]](https://python-poetry.org/) configuration file. This handles all of our project details and Python dependencies. We'll make some changes to this shortly.
6. Our main [Markdown [:material-arrow-right-bottom:]](https://www.markdownguide.org/getting-started/) file for explaining more about the project. You can think of this as the _face_ of the project. This is the first thing users will see when you publish your project to places like [GitHub [:material-arrow-right-bottom:]](https://github.com/) and [PyPi [:material-arrow-right-bottom:]](https://pypi.org/).
7. A [`Zentra`](#) configuration file to detect the root of your directory. This is used by the CLI to allow commands to be accessed anywhere in your project.

To keep things simple, we'll only focus on the main configuration files you need to address, but if you need more information you can check the `+` marks above. 

Most of the files are already pre-configured with your new project, but we do need to make some minor tweaks to make it unique to you!

### Poetry Configuration (pyproject.toml)

??? example "Example pyproject.toml"

    ```toml title=""
    [build-system]
    requires = ["poetry-core"]
    build-backend = "poetry.core.masonry.api"

    [tool.poetry]
    name = "app"
    version = "0.1.0"
    description = "A backend for processing API data."
    authors = ["Placeholder Name <placeholder@email.com>"]
    readme = "README.md"

    [tool.poetry.scripts]
    run-dev = "scripts.run:development"
    run-prod = "scripts.run:production"
    db-migrate = "scripts.db_migrate:main"

    [tool.poetry.dependencies]
    python = "^3.12"
    fastapi = "^0.112"
    sqlalchemy = "^2.0"
    alembic = "^1.13"
    pydantic-settings = "^2.4"
    pyjwt = "^2.9"
    bcrypt = "^4.2"

    [tool.poetry.group.dev.dependencies]
    pytest = "^8.3"
    pytest-cov = "^5.0"
    ```

Starting with the [`pyproject.toml`](#) file there is one major change you need to make - the **authors**. Make this bad boy unique to you 🤩!

```toml title="pyproject.toml" hl_lines="5"
[tool.poetry]
name = "app"
version = "0.1.0"
description = "A backend for processing API data."
authors = ["Placeholder Name <placeholder@email.com>"] # (1)!
readme = "README.md"
...
```

1. Update me!

The rest of the file is pretty common with the exception of [`tool.poetry.scripts`](#) and the project [`name`](#). 

The `name` is directly tied to the `app` directory and should only be changed when **desperately** needed. We use the name `app` by convention to indicate your _application_ code. 

!!! warning

    Changing the `app` name may break other parts of the project, such as `Alembic` so change it at your own risk.

The `poetry.scripts` are unique commands to your project and are connected to the `scripts` directory. They won't actually work yet until you install them (we'll get to that soon!). 

Interested in what they do? Check out the [Poetry Scripts](../../api/poetry-scripts.md) page.

### Environment Variables (.env file)

The `.env` file is an essential piece of the project for connecting the database and managing private information like API keys. 

Here's an example of what yours might look like with a project name of `deep_dive`:

```toml title=".env" hl_lines="6 9"
# Database details
DB__URL=sqlite:///./dev_db.db
# DB__URL=postgresql://user:password@postgresserver/db

DB__FIRST_SUPERUSER=admin@example.com
DB__FIRST_SUPERUSER_PASSWORD=p3qtC5sKhRHJjO3ydDVwfQ

# Authentication configuration details
AUTH__SECRET_KEY=JijXH8sD1d5x3T4sheWShqNDY64S3oIaMCHyJycOsPE

# Project settings
# This would be set to the production domain with an env var on deployment
DOMAIN=localhost

# Environment: local, staging, production
ENVIRONMENT=local

PROJECT_NAME=deep_dive
BACKEND_CORS_ORIGINS="http://localhost,http://localhost:8080"

# Emails
EMAIL__SMTP_HOST=
EMAIL__SMTP_USER=
EMAIL__SMTP_PASSWORD=
EMAIL__FROM_EMAIL=info@example.com
EMAIL__SMTP_TLS=True
EMAIL__SMTP_SSL=False
EMAIL__SMTP_PORT=587

# Docker
STACK_NAME=deep_dive-stack
DOCKER_IMAGE_BACKEND=backend
DOCKER_IMAGE_FRONTEND=frontend
```

The 😎 part about this file is that the highlighted lines are randomly generated on project creation. Zentra does all the work for you! ✨

!!! tip

    Desperately need a new `SECRET_KEY` or `PASSWORD`? Use the [`new-key`](../../api/commands/new-key.md) CLI commmand! 😏

To start with, you won't need to change this file unless you have a specific database in mind. By default we use a [SQLite [:material-arrow-right-bottom:]](https://www.sqlite.org/) database with [SQLAlchemy [:material-arrow-right-bottom:]](https://www.sqlalchemy.org/) for **development**.

In fact, we encourage and recommend you start with this approach and then transition to a [PostgreSQL [:material-arrow-right-bottom:]](https://www.postgresql.org/) database during **production**. It's the easiest to transition to and integrates seamlessly with our project setup.

## Tests Directory

```python title="Test Folder"
<project_name>/
...
├── tests/
│    ├── __init__.py
│    ├── conftest.py
│    └── test_auth.py
...
```

Home to your [Pytest [:material-arrow-right-bottom:]](https://docs.pytest.org/en/stable/) unit tests and other testing code. 

It already has a few files inside, one for user authentication (`test_auth.py`) and another for database (`conftest.py`) tests. These are generated automatically whenever you build a new API project to help you dive straight into your own code immediately. 

We encourage you to add to this folder when building up your application. We have a few plans to make testing easier in future versions, so stay tuned for that!

## Migrations Directory

```python title="Migrations Folder"
<project_name>/
...
├── migrations/
│    ├── env.py
│    ├── README
│    └── script.py.mako
...
```

A place for your [Alembic [:material-arrow-right-bottom:]](https://alembic.sqlalchemy.org/) database migrations. 

We've preconfigured this directory to work out of the box with your project, but you will need to make minor additions to the `env.py` file when making new database tables.

It's extremely easy to do, you only need to add `import` statements at the top of the file like the below:

```python title="migrations/env.py" hl_lines="8"
...
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.core.db import Base
from app.db_models.user import DBUser, DBUserDetails

# Add new imports here

load_dotenv()
...
```

This helps `Alembic` know which database tables it needs to manage. Admittedly, we sometimes forget to add this ourselves! 😅 So, we plan to automate this in a future version. 

## Scripts Directory

A folder dedicated to `poetry.scripts` used in the project. 

You can read more about this in the [Poetry Scripts](../../api/poetry-scripts.md) page.

## App Directory

Saving the best for last, our _application_ directory! Home to all of your API code, you'll be working in this folder constantly. From building new routes to database tables this folder really is the workhorse of the operation.

Here's what it looks like:

```python title="App Directory"
<project_name>/
├── app/
│   ├── api/
│   │   └── __init__.py
│   ├── auth/
│   │   └── __init__.py
│   │   └── responses.py
│   │   └── schema.py
│   ├── core/
│   │   └── __init__.py
│   │   └── config.py
│   │   └── db.py
│   │   └── dependencies.py
│   └── db_models/
│       └── __init__.py
│       └── user.py
...
```

This folder starts with four directories:

- [`api`](#) - a place to store all your API routes. We'll explore this in more detail in the next chapter - [Creating Routes](../../api/tutorial/create-routes.md).
- [`auth`](#) - files dedicated to user authentication. We discuss more about this in the [Authentication](../../api/tutorial/authentication.md) chapter.
- [`core`](#) - this contains all of our configuration settings for the project. Check out the [Project Settings](../../api/tutorial/settings.md) chapter for more details.
- [`db_models`](#) - our one-stop shop for our [SQLAlchemy [:material-arrow-right-bottom:]](https://www.sqlalchemy.org/) database models. We discuss this in more detail in the [Creating Tables](../../api/tutorial/create-tables.md) chapter.

## Starting Our Project

Whew! Okay, that was a lot to digest! Now that we have installed the project and are more familiar with it, we should probably check that our project works right?


1. Firstly, access the project directory:

    ??? note "Using `zentra-sdk`?"

        Access the FastAPI project using this instead:
        ```cmd title=""
        cd backend
        ```

    ```cmd title=""
    cd <project_name>
    ```

2. Next, install the poetry scripts and extra packages:

    ```cmd title=""
    poetry install
    ```

3. Test it works by running the development environment:

    ```cmd title=""
    run-dev
    ```

4. Navigate to [http://localhost:8080/api/docs](http://localhost:8080/api/docs) and you should see your authentication routes already configured!

![FastAPI setup example](../../assets/imgs/api/fastapi-auth-routes.jpg)

Awesome work! 👏 In the next chapter we'll start building some **API routes**. See you there!

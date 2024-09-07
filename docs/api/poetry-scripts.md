# Poetry Scripts

Poetry scripts are a way to create extra CLI commands inside Poetry projects. These are specifically designed for quickly executing small chunks of code with minimal effort.

Every new API project is preconfigured with a few unique ones stored inside the `pyproject.toml` file under `poetry.scripts`. 

These are directly connected to the `scripts` folder and only work when you have installed the your newly built project using the `install poetry` command. 

You can read more about this in the [First Steps](../api/tutorial/first-steps.md) tutorial.

=== "pyproject.toml"
    
    ```toml title=""
    ...
    [tool.poetry.scripts]
    run-dev = "scripts.run:development"
    run-prod = "scripts.run:production"
    db-migrate = "scripts.db_migrate:main"
    ...
    ```

=== "Related Files"

    ```cmd title="" hl_lines="6-8"
    <project_name>/
    ├── app/
    │   └── ...
    ├── migrations/
    │   └── ...
    ├── scripts/
    │   ├── db_migration.py
    │   └── run.py
    ├── tests/
    │    └── ...
    ...
    ```

So far, we've introduced 3 scripts to simplify specific operations.

## 1. run-dev

`run-dev` allows you to quickly run the [FastAPI [:material-arrow-right-bottom:]](https://fastapi.tiangolo.com/fastapi-cli/) **development** server on host `127.0.0.1:8080`. 

It's equivalent to this command:

```cmd title=""
fastapi dev app/main.py --port 8080
```

You'll often find yourself turning the development server on and off and repeating the full command can be very tedious. Well, now you don't have to worry about it!

## 2. run-prod

A compliment to `run-dev`, `run-prod` allows you to quickly run the [FastAPI [:material-arrow-right-bottom:]](https://fastapi.tiangolo.com/fastapi-cli/) **production** server on host `0.0.0.0:8080`.

It's equivalent to this command:

```cmd title=""
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

It's a great way to quickly spin-up your production server to test how your API performs in production, and to run the production environment in [Docker [:material-arrow-right-bottom:]](https://www.docker.com/resources/what-container/#:~:text=A%20Docker%20container%20image%20is,tools%2C%20system%20libraries%20and%20settings.) containers. 

## 3. db-migrate

`db-migrate` is a faster way to make [Alembic [:material-arrow-right-bottom:]](https://alembic.sqlalchemy.org/en/latest/) database migrations. 

Normally, you'd need to run two commands to make a single migration:

```python title=""
alembic revision --autogenerate -m "<description>"
alembic upgrade head
```

We wanted to simplify this process by compressing migrations into a single command. Now, all you need to do is run the following:

```python title=""
db-migrate "<description>"
```

The [`description`](#) explains what the database migration does. So for example, _create posts table_ or _update user table_. You can read more about migrations in the [Alembic [:material-arrow-right-bottom:]](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script) documentation.

When running the command, you'll be `prompted` to update the `head`. We can skip this prompt using the `--force` flag like so:

```python title=""
db-migrate "<description>" --force
```

This command has been a huge asset for improving our workflow and we hope you enjoy using it as much as we do!

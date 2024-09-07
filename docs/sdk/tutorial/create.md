# Creating a Project

Using the SDK is the easiest method for getting started with a new project.

Simply run the [`init`](/sdk/commands/init) command and you'll have a [FastAPI [:material-arrow-right-bottom:]](https://fastapi.tiangolo.com/) backend and [Next.js [:material-arrow-right-bottom:]](https://nextjs.org/) frontend in seconds! No extra parameters needed.

```cmd title=""
zentra init
```

You'll find two new shiny directories in your project folder that will look similar to this:

```cmd title=""
<project_name>/
├── backend/
│   ├── app/
│   │   └── ...
│   ├── ...
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
├── env/
│   └── ...
├── .gitignore
└── README.md
```

## Backend Directory

??? question "Did you know?"

    We built the backend using the [`zentra-api`](/api) package! 
    ```cmd title=""
    zentra-api init backend
    ```

    Pretty cool right?! 🤓

The backend directory is home to our `FastAPI` files and is fully managed by the [`zentra-api`](/api) package. 

You can read more about it in the API [First Steps](/api/tutorial/first-steps/) tutorial.

## Frontend Directory

The frontend directory contains our `Next.js` files and is unique to the SDK package.


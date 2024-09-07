# Zentra API

<div style="display: flex; justify-content: center; align-items: center;" markdown> 

[![codecov](https://codecov.io/github/Achronus/zentra-api/graph/badge.svg?token=Y2G1RM4WFO)](https://codecov.io/github/Achronus/zentra-api)
![Python Version](https://img.shields.io/pypi/pyversions/zentra-api)
![License](https://img.shields.io/github/license/Achronus/zentra-api)
![Issues](https://img.shields.io/github/issues/Achronus/zentra-api)
![Last Commit](https://img.shields.io/github/last-commit/Achronus/zentra-api)

</div>

---

<div id="quick-links" style="display: flex; justify-content: center; align-items: center; gap: 3rem">
    <a href="/api" target="_blank" style="text-align: center;">
        <svg xmlns="http://www.w3.org/2000/svg" height="32" width="28" viewBox="0 0 448 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="rgba(255, 255, 255, 0.7)" d="M96 0C43 0 0 43 0 96V416c0 53 43 96 96 96H384h32c17.7 0 32-14.3 32-32s-14.3-32-32-32V384c17.7 0 32-14.3 32-32V32c0-17.7-14.3-32-32-32H384 96zm0 384H352v64H96c-17.7 0-32-14.3-32-32s14.3-32 32-32zm32-240c0-8.8 7.2-16 16-16H336c8.8 0 16 7.2 16 16s-7.2 16-16 16H144c-8.8 0-16-7.2-16-16zm16 48H336c8.8 0 16 7.2 16 16s-7.2 16-16 16H144c-8.8 0-16-7.2-16-16s7.2-16 16-16z"/></svg>
        <p style="color: #fff; margin-top: 5px; margin-bottom: 5px;">Docs</p>
    </a>
    <a href="https://github.com/Achronus/zentra-api/" target="_blank"  style="text-align: center;">
        <svg xmlns="http://www.w3.org/2000/svg" height="32" width="28" viewBox="0 0 640 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="rgba(255, 255, 255, 0.7)" d="M392.8 1.2c-17-4.9-34.7 5-39.6 22l-128 448c-4.9 17 5 34.7 22 39.6s34.7-5 39.6-22l128-448c4.9-17-5-34.7-22-39.6zm80.6 120.1c-12.5 12.5-12.5 32.8 0 45.3L562.7 256l-89.4 89.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l112-112c12.5-12.5 12.5-32.8 0-45.3l-112-112c-12.5-12.5-32.8-12.5-45.3 0zm-306.7 0c-12.5-12.5-32.8-12.5-45.3 0l-112 112c-12.5 12.5-12.5 32.8 0 45.3l112 112c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L77.3 256l89.4-89.4c12.5-12.5 12.5-32.8 0-45.3z"/></svg>
        <p style="color: #fff; margin-top: 5px; margin-bottom: 5px;">Code</p>
    </a>
    <a href="https://pypi.org/project/zentra-api/" target="_blank"  style="text-align: center;">
        <svg xmlns="http://www.w3.org/2000/svg" height="32" width="28" viewBox="0 0 448 512"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="rgba(255, 255, 255, 0.7)" d="M439.8 200.5c-7.7-30.9-22.3-54.2-53.4-54.2h-40.1v47.4c0 36.8-31.2 67.8-66.8 67.8H172.7c-29.2 0-53.4 25-53.4 54.3v101.8c0 29 25.2 46 53.4 54.3 33.8 9.9 66.3 11.7 106.8 0 26.9-7.8 53.4-23.5 53.4-54.3v-40.7H226.2v-13.6h160.2c31.1 0 42.6-21.7 53.4-54.2 11.2-33.5 10.7-65.7 0-108.6zM286.2 404c11.1 0 20.1 9.1 20.1 20.3 0 11.3-9 20.4-20.1 20.4-11 0-20.1-9.2-20.1-20.4 .1-11.3 9.1-20.3 20.1-20.3zM167.8 248.1h106.8c29.7 0 53.4-24.5 53.4-54.3V91.9c0-29-24.4-50.7-53.4-55.6-35.8-5.9-74.7-5.6-106.8 .1-45.2 8-53.4 24.7-53.4 55.6v40.7h106.9v13.6h-147c-31.1 0-58.3 18.7-66.8 54.2-9.8 40.7-10.2 66.1 0 108.6 7.6 31.6 25.7 54.2 56.8 54.2H101v-48.8c0-35.3 30.5-66.4 66.8-66.4zm-6.7-142.6c-11.1 0-20.1-9.1-20.1-20.3 .1-11.3 9-20.4 20.1-20.4 11 0 20.1 9.2 20.1 20.4s-9 20.3-20.1 20.3z"/></svg>
        <p style="color: #fff; margin-top: 5px; margin-bottom: 5px;">PyPi</p>
    </a>
</div>

---

Zentra API is a powerful tool for building [FastAPI [:material-arrow-right-bottom:]](https://fastapi.tiangolo.com/) applications. 

It comes packed with it's own CLI tool and library that encourages rapid development and clean, pragmatic API design.

## What's Included?

When creating a project with [`zentra-api`](#) you immediately get access to the following:

- Built-in user authentication with JWT token protection
- Preconfigured CORs middleware
- A [SQLite [:material-arrow-right-bottom:]](https://www.sqlite.org/) database configured with [Alembic [:material-arrow-right-bottom:]](https://alembic.sqlalchemy.org/en/latest/) and [SQLAlchemy [:material-arrow-right-bottom:]](https://www.sqlalchemy.org/)
- Built-in templated route responses following best practices
- A simple folder structure to make project navigation a breeze
- Prebuilt [Pytests [:material-arrow-right-bottom:]](https://docs.pytest.org/en/stable/) so you can focus on your own code  
- And, access to our package filled with other goodies

But that's not all! We've also got plans to add:

- Rate limiting with [SlowAPI [:material-arrow-right-bottom:]](https://github.com/laurents/slowapi)
- API key configuration
- An admin interface for easily navigating your database
- Email based password recovery
- A [`build`](#) command to go from development to production in minutes
- And so much more...

## Getting Started

To get started, install the [`zentra-api`](#) package with [Poetry [:material-arrow-right-bottom:]](https://python-poetry.org/) through [PIP [:material-arrow-right-bottom:]](https://pypi.org/project/zentra-api/):

```cmd title=""
pip install zentra-api poetry
```

Next, click the button below to move onto our **User Guide** to learn how to get started with Zentra API.

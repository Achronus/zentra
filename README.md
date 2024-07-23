_Zentra is changing into something bigger and better..._

_We are still in development but are working hard to release a sample version soon._

![Logo](/docs/assets/imgs/zentra-logo.jpg)

Zentra, your all in one Python SDK for building [FastAPI](https://fastapi.tiangolo.com/) and [Next.js](https://nextjs.org/) applications faster.

# Zentra

Every new software project brings a familiar set of repetitive tasks: configuring API routes, setting up authentication, and crafting frontend components from scratch. These repetitive steps not only drain your time but also divert your focus from building the unique features that set your application apart.

What if you have 10 projects to build, or 100, or 1000? Imagine having to set up everything from scratch every single time. The constant cycle of boilerplate coding can be frustrating and counterproductive, leaving you bogged down in setup rather than innovating.

Introducing __Zentra__ — an open-source, free to use, SDK for rapidly creating [FastAPI](https://fastapi.tiangolo.com/) and [Next.js](https://nextjs.org/) applications.

Packed with an intuitive suite of CLI commands, documentation, and development kit, this tool simplifies your development process, allowing you to effortlessly build applications in weeks, not months.

## How It Works

Zentra is divided into three packages, allowing you to mix and match based on your requirements. These include:

- `API` - for FastAPI/backend development
- `Models` - for React.js component building
- `JS` - for Next.js/frontend development

Each package works independently so you can maximise their benefits with ease.

Perhaps you only want to build a FastAPI project, or simply want to build React components using Python - you choose what is right for you.

## API

Zentra API helps you build [FastAPI](https://fastapi.tiangolo.com/) projects faster.

It focuses on a CLI tool that simplifies the development process for generating routes and managing your application.

To get started, install the package with:

```bash
pip install zentra_api
```

Then create a new project with:

```bash
zentra-api init <project_name>
```

With one command you'll have a working app in minutes with:

- Built-in user authentication with JWT token protection
- Preconfigured CORs middleware
- A [SQLite](https://www.sqlite.org/) database configured with [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- Built-in templated route responses following best practices
- And, a simple folder structure to make project navigation a breeze

Read more about it in our [documentation](#) (_WIP_).

## Models

Zentra Models allows you to build React components using Python.

It uses [Pydantic](https://docs.pydantic.dev/latest/) models under-the-hood and focuses on utilising pre-built components to help you build your frontend structure faster.

It aims to be a flexible package that covers a variety of component libraries, while centering around the [NextJS App Router](https://nextjs.org/docs) framework.

Read more about it in our [documentation](#) (_WIP_).

## JS

TBC

## Active Development

Zentra is a tool that is continuously being developed. There's a lot still to do to make it a fully functioning SDK, such as a working CLI, detailed API documentation, and components for various libraries.

Our goal is to provide a quality open-source product that works 'out-of-the-box' that everyone can experiment with, and then gradually fix unexpected bugs and introduce more component libraries on the road to a `v1.0.0` release.

## Support

We'll need help from developers like you to make this tool a delight to use, and a product worthy of the `Python`, `NextJS`, `React` and `Software/Web Development` community.

Feedback and criticism will always be welcomed, and is encouraged to help make this tool worthwhile.

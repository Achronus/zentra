# Zentra SDK: Commands

This chapter focuses on the CLI commands you can use with the [`zentra-sdk`](#) package.

All commands must start with [`zentra`](#) when using this package.

??? tip "Reminder: Help Flag"
    All commands are configured with a `--help` flag that provides you with extra information about them. Simply add it to the command to read more information about it. For example:

    ```shell title=""
    zentra init --help
    ```

## Init

??? info "Noteworthy Features"

    - First use: adds the backend and frontend files
    - Additional uses: adds missing files to the directory

This command initialises the current directory as a `Zentra` project, configuring it with a [FastAPI [:material-arrow-right-bottom:]](https://fastapi.tiangolo.com/) backend and [Next.js [:material-arrow-right-bottom:]](https://nextjs.org/) frontend.

```shell title=""
zentra init
```

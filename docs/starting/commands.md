# Commands

You will often interact with `Zentra` using its command-line interface (CLI). This chapter documents all the available commands `Zentra` has to offer.

!!! note
    All commands are configured with a `--help` flag that provides you with extra information about them. Simply add it to the command to read more information about it. For example:

    ```shell title=""
    zentra init --help
    ```

## Error Messages

We've designed the CLI to provide useful feedback when an `error` occurs. Our aim with `Zentra` is to allow users to focus on programming there project with minimal interference.

As such, our error messages will help you quickly fix issues yourself (if possible). We explain more about them in our [Error Handling Guide](../help/errors.md).

We encourage you to check this out when the time is right!

## Global Options

This section contains a list of flags that are applicable to every command.

- `--help (-h)` - displays help information

## zentra init

This command initialises the current directory as a `Zentra` project, configuring it with specific files required for using `Zentra`.

Normally, you would use it without any arguments like so:

```shell title=""
zentra init
```

This requires confirmation to initialise the application and is the recommended approach to running the command.

It also comes with an optional `--force` flag to ignore the user input. This is useful when you want to use `Zentra` in other applications such as our [Create API App](#zentra-init) tool.

```shell title=""
zentra init --force
```

You can read more about the [`zentra init`](#zentra-init) command in our [Basic Usage Guide](basic_usage.md#creating-a-project).

## zentra generate

This is the main command you will run when using `Zentra`. It creates and updates your `React` components by reading the information in the `Zentra` app.

```shell title=""
zentra generate
```

You can read more about it in our [Basic Usage Guide](basic_usage.md#generating-components).

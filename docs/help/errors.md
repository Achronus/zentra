# Encountering Errors

Like any program or tool, encountering errors can be very frustrating, and typically, unavoidable.

While we've taken great care to mitigate running into errors when using `Zentra`, they can still occur. People use tools in different ways and it can be extremely difficult to interpret how someone will use the tool for their own benefit.

Rather than blindly asking everyone to post their issues on the GitHub repo, we've curated a list of error messages that you may encounter when using the tool.

We encourage everyone to refer to this list and use it as a guideline first, before posting an issue on GitHub.

## How This Guide Works

We've designed our error messages to be as informative as possible so that you can solve the issue yourself without any external intervention. Normally, this will suffice but there are rare circumstances where that won't be the case.

Each error will come with a code that will help you navigate to a part of this page for details on why the error is happening and how you could potentially solve it.

Simply use the find (`Ctrl + f` on Windows, Linux and ChromeOS, or `cmd + f` on Mac) function in your browser. Then, copy and paste the `Error Code: [number]` to find it on the page.

If you've encountered something extremely mind boggling (trust me, you'll know :wink:), please follow our [Reporting Issues Guide](report.md).

## Types of Errors

Error messages are split into three main categories:

- [`common`](#common-errors) - errors that can occur across all commands
- [`setup`](#setup-errors) - errors specific to the [`zentra init`](../starting/commands.md#zentra-init) command
- [`generate`](#generate-errors) - errors specific to the [`zentra generate`](../starting/commands.md#zentra-generate) commands

## Common Errors

### 1: Config File Missing

`Error Code: 1`

You'll encounter this error when the `__init__.py` file is missing from the `zentra/models` directory.

To fix it, run the [`zentra init`](../starting/commands.md#zentra-init) command to create a new `config` file.

### 2: Config File Empty

`Error Code: 2`

You'll encounter this error when the `__init__.py` file in the `zentra/models` directory is empty.

To fix it, run [`zentra init --reset-config`](../starting/commands.md#zentra-init) to create a new one.

### 3: Zentra Directory Missing

`Error Code: 3`

You'll encounter this error when you have the `Zentra` package installed but haven't initialised the project yet.

To fix it, run the [`zentra init`](../starting/commands.md#zentra-init) command.

### 4: Models Directory Missing

`Error Code: 4`

You'll encounter this error when the `zentra/models` directory is missing.

To fix it, run the [`zentra init`](../starting/commands.md#zentra-init) command.

### 5: No Components Found

`Error Code: 5`

You'll encounter this error when the `Zentra` app cannot find any `React` components to create.

To fix it, open the config file at `zentra/models/__init__.py` and perform the following checks:

1. `zentra = Zentra()` is initialised
2. You've registered some `components` or `pages` using `zentra.register()`

If you are still experiencing issues, please reset the config file with [`zentra init --reset-config`](../starting/commands.md#zentra-init).

### 1000: Unknown Error

`Error Code: 1000`

You'll encounter this error when something happens that we haven't accounted for.

For these types of errors, please follow our [Reporting Issues Guide](report.md).

## Setup Errors

### 11: Import Error

`Error Code: 11`

You'll encounter this error when failing to find the `Zentra` app in `zentra/models/__init__.py`.

To fix it, perform one of the following:

1. If the file exists, initialise `zentra = Zentra()`
2. Reset the config file with [`zentra init --reset-config`](../starting/commands.md#zentra-init)

## Generate Errors


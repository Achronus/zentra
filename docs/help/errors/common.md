# Common Errors

These types of errors can commonly occur across all commands and packages and range between `[1, 10]`.

## 1: Config File Missing

`Error Code: 1`

You'll encounter this error when the `__init__.py` file is missing from the `zentra/models` directory.

To fix it, run the [`zentra init`](#) command to create a new `config` file.

## 2: Config File Empty

`Error Code: 2`

You'll encounter this error when the `__init__.py` file in the `zentra/models` directory is empty.

To fix it, run [`zentra init --reset-config`](#) to create a new one.

## 3: Zentra Directory Missing

`Error Code: 3`

You'll encounter this error when you have the `Zentra` package installed but haven't initialised the project yet.

To fix it, run the [`zentra init`](#) command.

## 4: Models Directory Missing

`Error Code: 4`

You'll encounter this error when the `zentra/models` directory is missing.

To fix it, run the [`zentra init`](#) command.

## 5: No Components Found

`Error Code: 5`

You'll encounter this error when the `Zentra` app cannot find any `React` components to create.

To fix it, open the config file at `zentra/models/__init__.py` and perform the following checks:

1. `zentra = Zentra()` is initialised
2. You've registered some `components` or `pages` using `zentra.register()`

If you are still experiencing issues, please reset the config file with [`zentra init --reset-config`](#).

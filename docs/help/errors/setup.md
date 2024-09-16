# Setup Errors

These types of errors are unique to the [`init`](#) command but can occur across all and packages. These errors range between `[11, 20]`.

## 11: Import Error

`Error Code: 11`

You'll encounter this error when failing to find the `Zentra` app in `zentra/models/__init__.py`.

To fix it, perform one of the following:

1. If the file exists, initialise `zentra = Zentra()`
2. Reset the config file with [`zentra init --reset-config`](#)


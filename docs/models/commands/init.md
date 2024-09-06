# Init

??? info "Noteworthy Features"

    - First use: configures the directory as a `Zentra` project
    - Additional uses: adds missing configuration files to the `zentra` directory

This command initialises the current directory as a `Zentra` project, configuring it with the specific files required for using `Zentra`.

```shell title=""
zentra-api init <project_name>
```

This requires confirmation to initialise the application and is the recommended approach to running the command.

### Init: Optional Flags

!!! warning
    When using `--reset-config` all its content is reset back to the default template. You __will lose__ the existing content inside of it.

| Flag             | Description |
|------------------|-------------|
|`--force`         | removes confirmation requirement. Also, works with `--reset-config`. |
| `--reset-config` | hard resets the `zentra/models/__init__.py` file. |

You can read more about the [`zentra init`](#zentra-init) command in our [Basic Usage Guide](basic_usage.md#creating-a-project).
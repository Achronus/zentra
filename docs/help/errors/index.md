# Errors

Like any program or tool, encountering errors can be very frustrating, and typically, unavoidable.

While we've taken great care to mitigate running into errors when using `Zentra`, they can still occur. People use tools in different ways and it can be extremely difficult to interpret how someone will use the tool for their own benefit.

Rather than blindly asking everyone to post their issues on the GitHub repo, we've curated a list of error messages that you may encounter when using the tool.

We encourage everyone to refer to this list and use it as a guideline first, before posting an issue on GitHub.

## How This Guide Works

We've designed our error messages to be as informative as possible so that you can solve the issue yourself without any external intervention. Normally, this will suffice but there are rare circumstances where that won't be the case.

Each error will come with a code that will help you navigate to a part of this page for details on why the error is happening and how you could potentially solve it.

Simply use the find (`Ctrl + f` on Windows, Linux and ChromeOS, or `cmd + f` on Mac) function in your browser. Then, copy and paste the `Error Code: [number]` to find it on the page.

If you've encountered something extremely mind boggling (trust me, you'll know :wink:), please follow our [Reporting Issues Guide](../report.md).

## Types of Errors

Error messages are split into three main categories:

- [`common`](../errors/common.md) - errors that can occur across all commands and packages. These range between `[1, 10]`
- [`setup`](../errors/setup.md) - errors specific to the [`init`](#) command. These range between `[11, 20]`.
- [`build`](../errors/build.md) - errors specific to the [`generate`](#) and [`build`](#) commands. These range between `[21, 30]`.

## 1000: Unknown Error

`Error Code: 1000`

You'll encounter this error when something happens that we haven't accounted for.

For these types of errors, please follow our [Reporting Issues Guide](../report.md).

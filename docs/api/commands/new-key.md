# New Key

???+ info "Noteworthy Features"

    - Every use: generates a new secret key.

This command creates a new randomly generated URL-safe token[^1] using Base64 encoding.

```shell title=""
new-key
```

## Optional Parameters

| Parameter   | Type    | Description                      |  Default |
|-------------|---------|----------------------------------|----------|
|`size`       | Integer | The number of bytes to generate. Each byte is approximately 1.3 characters. | 32       |


[^1]: A URL-safe token is a string safe for use in URLs by avoiding characters that might require special encoding such as `+`, `/`, or `=`. 

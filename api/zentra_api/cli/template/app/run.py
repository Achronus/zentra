import argparse

import uvicorn


def development(host: str = "127.0.0.1", port: int = 8000) -> None:
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        workers=1,
        limit_concurrency=1,
        limit_max_requests=1,
    )


def production(host: str = "0.0.0.0", port: int = 8000) -> None:
    uvicorn.run("app.main:app", host=host, port=port)


def start(env_mode, host: str, port: int) -> None:
    """Start the server."""
    if env_mode == "dev":
        development(host=host, port=port)
    else:
        production(host=host, port=port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start the server.")
    parser.add_argument(
        "-e", "--env", type=str, default="dev", choices=["dev", "prod"], required=True
    )
    parser.add_argument("-ht", "--host", type=str, default="127.0.0.1", required=False)
    parser.add_argument("-pt", "--port", type=int, default=8000, required=False)

    args = parser.parse_args()
    start(env_mode=args.env, host=args.host, port=args.port)

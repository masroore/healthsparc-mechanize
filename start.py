import logging
import os
from logging.config import fileConfig
import pathlib
import uvicorn


def set_uvicorn_options(
    app_module: str,
) -> dict:
    """Set options for running the Uvicorn server."""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    log_level = os.getenv("LOG_LEVEL", "info")
    use_reload = bool((value := os.getenv("WITH_RELOAD")) and value.lower() == "true")
    reload_delay = float(value) if (value := os.getenv("RELOAD_DELAY")) else 0.25
    uvicorn_options = {
        "app": app_module,
        "host": host,
        "port": port,
        "log_level": log_level,
        "reload": use_reload,
        "reload_delay": reload_delay,
    }
    return uvicorn_options


def start_server(
    app_module: str,
    logger: logging.Logger = logging.getLogger(),
) -> None:
    """Start the Uvicorn or Gunicorn server."""
    try:
        logger.debug("Starting uvicorn server...")
        uvicorn_options = set_uvicorn_options(app_module)
        uvicorn.run(**uvicorn_options)
    except Exception as e:
        logger.error(f"Error when starting server: {e.__class__.__name__} {e}.")
        raise


if __name__ == "__main__":
    fileConfig(str(pathlib.Path('./conf/logging.ini').resolve()))
    logger = logging.getLogger()
    start_server(
        app_module="main:app",
        logger=logger,
    )

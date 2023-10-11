import logging
import pathlib
from logging.config import fileConfig

import uvicorn

from src import config

MAIN_DIR = pathlib.Path(__file__).parent
CONFIG_DIR = MAIN_DIR / "conf"


def set_uvicorn_options() -> dict:
    conf = config.load_config("site.yaml")

    """Set options for running the Uvicorn server."""
    app_module = conf["uvicorn"]["app"]
    host = conf["uvicorn"]["host"]
    port = int(value) if (value := conf["uvicorn"]["port"]) else 8000
    log_level = conf["uvicorn"]["log_level"]
    use_reload = conf["uvicorn"]["with_reload"]
    reload_delay = float(value) if (value := conf["uvicorn"]["reload_delay"]) else 0.25
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
    logger: logging.Logger = logging.getLogger(),
) -> None:
    """Start the Uvicorn or Gunicorn server."""
    try:
        logger.debug("Starting uvicorn server...")
        uvicorn_options = set_uvicorn_options()
        uvicorn.run(**uvicorn_options)
    except Exception as e:
        logger.error(f"Error when starting server: {e.__class__.__name__} {e}.")
        raise


def get_logger():
    fileConfig(str((CONFIG_DIR / "logging.ini").resolve()))
    return logging.getLogger()


if __name__ == "__main__":
    logger = get_logger()
    start_server(logger=logger)

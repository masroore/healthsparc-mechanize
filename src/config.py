from typing import Any

import yaml
from pathlib import Path

conf_dir = Path("./conf").absolute()


def pathify(filename: str) -> Path:
    fpath = conf_dir.joinpath(filename)
    return fpath


def load_config(filename: str) -> Any:
    with pathify(filename).open("r") as fp:
        return yaml.safe_load(fp)

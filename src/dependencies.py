from fastapi import Request, Depends
from pyodbc import Connection

from src import db, config


async def _get_db():
    conn = db.connect(config=config.load_config("db.yaml"))
    try:
        yield conn
    finally:
        db.close()


async def get_db(request: Request, db: Connection = Depends(_get_db)) -> None:
    request.state.db = db

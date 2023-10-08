from typing import Any, Annotated
from logging.config import fileConfig
from fastapi import FastAPI, Depends
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

from src import dal, db, config, auth

site_config = config.load_config("site.yaml")
APP_NAME = site_config["app_name"]
SITE_ID = site_config["site_id"]

auth.set_credentials(site_config["auth"]["username"], site_config["auth"]["password"])

HttpBasicAuth = Annotated[str, Depends(auth.authenticate)]


def get_db():
    conn = db.connect(config=config.load_config("db.yaml"))
    try:
        yield conn
    finally:
        db.close()


middleware = [
    Middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_headers=["*"],
        allow_methods=["*"],
    )
]
app = FastAPI(middleware=middleware, title=APP_NAME)


@app.get("/", status_code=status.HTTP_200_OK)
async def root() -> str:
    return "Hello, world!"


@app.get("/status", status_code=status.HTTP_200_OK)
async def status(credentials: HttpBasicAuth) -> dict:
    return {
        "app": APP_NAME,
        "status": "active",
        "user": auth.get_username(),
    }


@app.get("/procedures")
async def procedures(auth: HttpBasicAuth, db: Any = Depends(get_db)):
    rows = dal.procedures_catalog()
    return rows


@app.get("/referrers")
async def referrers(db: Any = Depends(get_db)):
    rows = dal.referrers_catalog()
    return rows


@app.get("/invoice/{invoice_id}")
async def order(invoice_id: int, db: Any = Depends(get_db)):
    order_details = dal.lab_order_details(invoice_id=invoice_id)
    return order_details


@app.get("/bundles/{invoice_id}")
async def order(invoice_id: int, db: Any = Depends(get_db)):
    rows = dal.lab_order_result_bundles(invoice_id=invoice_id)
    return rows

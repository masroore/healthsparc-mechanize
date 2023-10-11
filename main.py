from typing import Any, Annotated

from fastapi import FastAPI, Depends
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

from src import db, config, auth, dependencies
from src.dal import catalog, proe

site_config = config.load_config("site.yaml")
APP_NAME = site_config["app_name"]
SITE_ID = site_config["site_id"]

auth.set_credentials(site_config["auth"]["username"], site_config["auth"]["password"])

HttpBasicAuth = Annotated[str, Depends(auth.authenticate)]

app = FastAPI(
    dependencies=[
        Depends(dependencies.get_db),
    ],
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_origins=["*"],
            allow_headers=["*"],
            allow_methods=["*"],
        )
    ],
    title=APP_NAME,
)


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
async def procedures(credentials: HttpBasicAuth):
    rows = catalog.get_procedures()
    return rows


@app.get("/referrers")
async def referrers(credentials: HttpBasicAuth):
    rows = catalog.get_referrers()
    return rows


@app.get("/invoice/{invoice_id}")
async def order(invoice_id: int, credentials: HttpBasicAuth):
    order_details = proe.lab_order_details(invoice_id=invoice_id)
    return order_details


@app.get("/bundles/{invoice_id}")
async def order(invoice_id: int, credentials: HttpBasicAuth):
    rows = proe.lab_order_result_bundles(invoice_id=invoice_id)
    return rows

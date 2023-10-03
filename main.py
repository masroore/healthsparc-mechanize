from typing import Any

from fastapi import FastAPI, Depends
from src import dal, db, config

app = FastAPI()

SITE_ID = config.load_config("site.yaml")["site_id"]


def get_db():
    conn = db.connect(config=config.load_config("db.yaml"))
    try:
        yield conn
    finally:
        db.close()


@app.get("/procedures")
async def procedures(db: Any = Depends(get_db)):
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

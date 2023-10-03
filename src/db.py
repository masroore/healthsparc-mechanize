from typing import Any

import pyodbc

_conn: pyodbc.Connection | None = None


def connect(config: dict) -> pyodbc.Connection:
    global _conn
    conn_string = ";".join("=".join([k, v]) for k, v in config.items())
    _conn = pyodbc.connect(conn_string)
    return _conn


def fetch_all(sql: str, *params: Any) -> list[dict]:
    cur = _conn.cursor()
    cur.execute(sql, params)

    cols = [c[0] for c in cur.description]

    results = []
    for row in cur.fetchall():
        results.append(dict(zip(cols, row)))

    return results


def fetch(sql: str, *params: Any) -> dict:
    cur = _conn.cursor()
    cur.execute(sql, params)

    cols = [c[0] for c in cur.description]
    row = cur.fetchone()

    return dict(zip(cols, row))


def close():
    global _conn
    _conn.close()
    _conn = None

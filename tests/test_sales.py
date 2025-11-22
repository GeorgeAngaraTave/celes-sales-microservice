from datetime import datetime
import pandas as pd
from fastapi.testclient import TestClient

from app.main import app
from app.services import datamart

client = TestClient(app)


def setup_module(_module):
    data = {
        "KeyEmployee": [1, 1, 2],
        "KeyProduct": [10, 11, 10],
        "KeyStore": [100, 100, 200],
        "KeyDate": [
            datetime(2023, 1, 1),
            datetime(2023, 1, 2),
            datetime(2023, 1, 3),
        ],
        "Amount": [100.0, 200.0, 300.0],
    }
    df = pd.DataFrame(data)

    datamart.load_datamart.cache_clear()
    datamart.load_datamart.__wrapped__ = lambda: df  # type: ignore


def _get_token():
    resp = client.post(
        "/auth/login",
        data={"username": "admin", "password": "admin"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 200
    return resp.json()["access_token"]


def test_sales_by_employee():
    token = _get_token()
    resp = client.get(
        "/sales/employee",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    totals = {item["key"]: item["total_sales"] for item in data}
    assert totals[1] == 300.0
    assert totals[2] == 300.0


def test_sales_by_product():
    token = _get_token()
    resp = client.get(
        "/sales/product",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200


def test_sales_by_store():
    token = _get_token()
    resp = client.get(
        "/sales/store",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
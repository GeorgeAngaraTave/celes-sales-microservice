from typing import Optional, List

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from ..core.security import get_current_user
from ..services.datamart import sales_by_dimension, sales_summary_by_dimension

router = APIRouter()


class SalesItem(BaseModel):
    key: str = Field(..., description="Identificador (KeyEmployee, KeyProduct o KeyStore)")
    total_sales: float


class SalesSummaryItem(BaseModel):
    key: str = Field(..., description="Identificador (KeyEmployee, KeyProduct o KeyStore)")
    total_sales: float
    average_sales: float


def _normalize_records(records):
    normalized = []
    for r in records:
        key_field = [k for k in r.keys() if k not in ("total_sales", "average_sales")][0]
        new_item = {
            "key": str(r[key_field]),
            "total_sales": r.get("total_sales"),
        }
        if "average_sales" in r:
            new_item["average_sales"] = r["average_sales"]
        normalized.append(new_item)
    return normalized


@router.get("/employee", response_model=List[SalesItem])
async def sales_by_employee(
    start_date: Optional[str] = Query(None, description="Fecha inicial YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="Fecha final YYYY-MM-DD"),
    _: dict = Depends(get_current_user),
):
    records = sales_by_dimension("KeyEmployee", start_date, end_date)
    return _normalize_records(records)


@router.get("/product", response_model=List[SalesItem])
async def sales_by_product(
    start_date: Optional[str] = Query(None, description="Fecha inicial YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="Fecha final YYYY-MM-DD"),
    _: dict = Depends(get_current_user),
):
    records = sales_by_dimension("KeyProduct", start_date, end_date)
    return _normalize_records(records)


@router.get("/store", response_model=List[SalesItem])
async def sales_by_store(
    start_date: Optional[str] = Query(None, description="Fecha inicial YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="Fecha final YYYY-MM-DD"),
    _: dict = Depends(get_current_user),
):
    records = sales_by_dimension("KeyStore", start_date, end_date)
    return _normalize_records(records)


@router.get("/employee/summary", response_model=List[SalesSummaryItem])
async def sales_summary_employee(
    start_date: Optional[str] = Query(None, description="Fecha inicial YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="Fecha final YYYY-MM-DD"),
    _: dict = Depends(get_current_user),
):
    records = sales_summary_by_dimension("KeyEmployee", start_date, end_date)
    return _normalize_records(records)


@router.get("/product/summary", response_model=List[SalesSummaryItem])
async def sales_summary_product(
    start_date: Optional[str] = Query(None, description="Fecha inicial YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="Fecha final YYYY-MM-DD"),
    _: dict = Depends(get_current_user),
):
    records = sales_summary_by_dimension("KeyProduct", start_date, end_date)
    return _normalize_records(records)


@router.get("/store/summary", response_model=List[SalesSummaryItem])
async def sales_summary_store(
    start_date: Optional[str] = Query(None, description="Fecha inicial YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="Fecha final YYYY-MM-DD"),
    _: dict = Depends(get_current_user),
):
    records = sales_summary_by_dimension("KeyStore", start_date, end_date)
    return _normalize_records(records)

from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

import pandas as pd

from ..core.config import settings


DimensionType = Literal["KeyEmployee", "KeyProduct", "KeyStore"]


@lru_cache(maxsize=1)
def load_datamart() -> pd.DataFrame:
    """Carga todos los archivos Parquet del datamart y los concatena en un DataFrame.

    El path se toma de settings.datamart_path. Usa cache simple en memoria.
    """
    base = Path(settings.datamart_path)
    if not base.exists():
        raise FileNotFoundError(f"No se encontró la ruta del datamart: {base.resolve()}")

    files = sorted(base.glob("*.parquet"))
    if not files:
        raise FileNotFoundError(f"No se encontraron archivos .parquet en {base.resolve()}")

    dfs = [pd.read_parquet(str(f)) for f in files]
    df = pd.concat(dfs, ignore_index=True)

    # Normaliza fechas a datetime; vienen como 'YYYY-MM-DD'
    df[settings.date_column] = pd.to_datetime(
        df[settings.date_column].astype(str),
        format="%Y-%m-%d",
        errors="coerce",
    )

    return df


def filter_by_period(
    df: pd.DataFrame,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """Filtra el DataFrame por un rango de fechas (inclusive)."""
    if start_date:
        df = df[df[settings.date_column] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df[settings.date_column] <= pd.to_datetime(end_date)]
    return df


def sales_by_dimension(
    dimension: DimensionType,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """Retorna las ventas agregadas por una dimensión en un periodo.

    Suma las ventas (`Amount`) agrupando por la dimensión indicada.
    """
    df = load_datamart()
    df = filter_by_period(df, start_date, end_date)

    grouped = (
        df.groupby(dimension)[settings.amount_column]
        .sum()
        .reset_index()
        .rename(columns={settings.amount_column: "total_sales"})
    )
    return grouped.to_dict(orient="records")


def sales_summary_by_dimension(
    dimension: DimensionType,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    """Retorna total y promedio de ventas por una dimensión en un periodo."""
    df = load_datamart()
    df = filter_by_period(df, start_date, end_date)

    grouped = df.groupby(dimension)[settings.amount_column].agg(["sum", "mean"]).reset_index()
    grouped = grouped.rename(columns={"sum": "total_sales", "mean": "average_sales"})
    return grouped.to_dict(orient="records")

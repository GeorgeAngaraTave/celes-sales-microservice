from datetime import datetime
import pandas as pd
from fastapi.testclient import TestClient
from app.main import app
from app.services import datamart
from unittest.mock import patch

client = TestClient(app)

def setup_module(module):
    """
    Prepara un datamart mockeado y evita que load_datamart real se ejecute.
    Funciona correctamente dentro de GitHub Actions.
    """

    # 1. Borrar cache del decorador lru_cache
    datamart.load_datamart.cache_clear()

    # 2. Crear DataFrame mock
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

    # 3. Reemplazar load_datamart dentro del módulo real
    module.load_datamart_patcher = patch(
        "app.services.datamart.load_datamart",
        return_value=df
    )
    module.load_datamart_patcher.start()

def teardown_module(module):
    """
    Detener el parcheo al final.
    """
    module.load_datamart_patcher.stop()
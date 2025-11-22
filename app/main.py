from fastapi import FastAPI
from .api.routes_auth import router as auth_router
from .api.routes_sales import router as sales_router

app = FastAPI(
    title="Prueba Técnica - Python Developer",
    version="1.0.0",
    description="Microservicio para la prueba técnica de Celes usando FastAPI, JWT y Parquet.",
)

# Ruta pública, no requiere autenticación
@app.get("/")
async def read_root():
    return {"message": "Prueba Técnica - Python Developer"}
# Incluir rutas de autenticación y ventas
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(sales_router, prefix="/sales", tags=["Sales"])

from typing import Optional
from pydantic import Field
from pydantic import BaseSettings
from dotenv import load_dotenv


# Cargar las variables del .env ANTES de que Pydantic intente leerlas
load_dotenv()

class Settings(BaseSettings):
    secret_key: str = Field("change-me", env="SECRET_KEY")
    algorithm: str = Field("HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    datamart_path: str =  Field("./data", env="DATAMART_PATH")
    # Ajustado al esquema real 
    date_column: str = Field("KeyDate", env="DATE_COLUMN")
    amount_column: str = Field("Amount", env="AMOUNT_COLUMN")

    # Puede haber archivo o usar credenciales por defecto de GCP
    firebase_credentials_file: str = Field(None, env="FIREBASE_CREDENTIALS_FILE")
    firebase_project_id: str = Field("tu-project-id", env="FIREBASE_PROJECT_ID")

    class Config:
        env_file = ".env"


settings = Settings()

"""
config.py - Configuración centralizada de la aplicación.
Principio SOLID: SRP - Una única responsabilidad: gestionar configuración.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuración de la aplicación cargada desde variables de entorno."""

    # Base de datos
    database_url: str = "postgresql://user:pass@localhost/factuplus"

    # Seguridad JWT
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # DIAN (Simulacro)
    dian_api_url: str = "https://vpfe-hab.dian.gov.co/WcfDianCustomerServices.svc"
    dian_api_key: str = "test-dian-key"

    # Aplicación
    app_name: str = "FactuPlus"
    app_version: str = "1.0.0"
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna la instancia única de Settings (compatible con Singleton via lru_cache).
    El decorador lru_cache garantiza que solo se crea una instancia.
    """
    return Settings()
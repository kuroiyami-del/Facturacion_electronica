"""
main.py - Punto de entrada de la aplicación FastAPI FactuPlus.

Inicializa el servidor, registra routers y configura CORS para el frontend React.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database.connection import DatabaseConnection
from app.database.base import Base

# Importar todos los modelos para que SQLAlchemy los registre antes de create_all
import app.models  # noqa: F401

from app.routers import auth, clientes, productos, facturas

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ciclo de vida de la aplicación: startup y shutdown."""
    settings = get_settings()
    logger.info("🚀 Iniciando %s v%s", settings.app_name, settings.app_version)

    # Crear tablas en la base de datos si no existen
    db_conn = DatabaseConnection.get_instance()
    Base.metadata.create_all(bind=db_conn.engine)
    logger.info("✅ Base de datos conectada y tablas verificadas.")

    yield  # La aplicación está en ejecución aquí

    logger.info("⏹️  Cerrando %s...", settings.app_name)


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Sistema de Facturación Electrónica con integración DIAN. "
        "Implementa patrones Singleton, Factory, Repository, Observer y Strategy."
    ),
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # React development server
        "http://localhost:5173",   # Vite development server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
API_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(clientes.router, prefix=API_PREFIX)
app.include_router(productos.router, prefix=API_PREFIX)
app.include_router(facturas.router, prefix=API_PREFIX)


@app.get("/", tags=["Health"])
def health_check():
    """Endpoint de verificación de estado del servidor."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
    }
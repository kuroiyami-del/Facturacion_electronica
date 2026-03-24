"""
database/connection.py - Patrón Singleton para la conexión a la base de datos.

Principio SOLID aplicado:
  - SRP: Este módulo tiene una única responsabilidad — gestionar la conexión a la BD.
  - DIP: El resto de la aplicación depende de esta abstracción, no de implementaciones concretas.

Patrón de Diseño: Singleton
  - Garantiza que exista una única instancia del motor de base de datos en toda la aplicación.
  - Evita la apertura excesiva de conexiones y centraliza la configuración.
"""
import threading
from typing import Generator

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import get_settings


class DatabaseConnection:
    """
    Implementación del patrón Singleton para la conexión a PostgreSQL vía SQLAlchemy.
    
    Uso:
        db = DatabaseConnection.get_instance()
        session = db.get_session()
    """

    _instance: "DatabaseConnection | None" = None
    _lock: threading.Lock = threading.Lock()

    def __init__(self) -> None:
        """Constructor privado — no llamar directamente. Usar get_instance()."""
        settings = get_settings()
        self._engine: Engine = create_engine(
            settings.database_url,
            pool_pre_ping=True,       # Verifica la conexión antes de usarla
            pool_size=10,             # Conexiones simultáneas máximas
            max_overflow=20,          # Conexiones extra temporales
            echo=settings.debug,      # Loguea SQL en modo debug
        )
        self._SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
        )

    @classmethod
    def get_instance(cls) -> "DatabaseConnection":
        """
        Retorna la instancia única de DatabaseConnection.
        Thread-safe gracias al doble bloqueo (Double-Checked Locking).
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Segunda verificación dentro del lock
                    cls._instance = cls()
        return cls._instance

    @property
    def engine(self) -> Engine:
        """Expone el engine de SQLAlchemy para crear tablas y migraciones."""
        return self._engine

    def get_session(self) -> Session:
        """Crea y retorna una nueva sesión de base de datos."""
        return self._SessionLocal()


def get_db() -> Generator[Session, None, None]:
    """
    Dependencia de FastAPI para inyección de sesión de base de datos.
    
    Garantiza que la sesión se cierre correctamente después de cada request,
    incluso si ocurre una excepción.
    
    Uso en routers:
        @router.get("/items")
        def list_items(db: Session = Depends(get_db)):
            ...
    """
    db_connection = DatabaseConnection.get_instance()
    session = db_connection.get_session()
    try:
        yield session
    finally:
        session.close()
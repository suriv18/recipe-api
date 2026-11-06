
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from recipe_api.core.config import settings


# Motor de conexión a PostgreSQL
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    echo=False
)


# Fábrica de sesiones
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)


# Clase base de los modelos ORM
class Base(DeclarativeBase):
    pass


# Dependencia para obtener sesiones
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

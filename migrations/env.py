from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from recipe_api.core.config import settings
from recipe_api.core.database import Base

# Importamos los modelos para que SQLAlchemy los registre
from recipe_api.modules.areas.model import Area
from recipe_api.modules.categories.model import Category
from recipe_api.modules.units.model import Unit
from recipe_api.modules.ingredients.model import Ingredient
from recipe_api.modules.recipes.model import Recipe
from recipe_api.modules.steps.model import Step
from recipe_api.modules.recipe_ingredients.model import RecipeIngredient


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Metadata que Alembic utilizará para detectar las tablas
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Ejecuta migraciones sin crear una conexión real."""

    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta migraciones conectándose a PostgreSQL."""

    connectable = create_engine(
        settings.database_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
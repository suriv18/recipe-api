# Recipe API

API REST para la gestión de recetas, construida con **FastAPI**, **SQLAlchemy** y **PostgreSQL 18**.

## Stack

| Componente | Función |
| --- | --- |
| Python 3.15 | Lenguaje |
| [uv](https://docs.astral.sh/uv/) | Gestor de paquetes y entorno virtual |
| FastAPI + Uvicorn | Framework web y servidor ASGI |
| SQLAlchemy | ORM para representar tablas como clases Python |
| Alembic | Migraciones de la base de datos |
| psycopg (binary) | Controlador Python ↔ PostgreSQL |
| pydantic-settings | Lectura y validación de variables de configuración |
| Docker Compose | Base de datos PostgreSQL 18 en contenedor |

## Requisitos previos

- Python 3.15 (uv lo descarga si no lo encuentra)
- uv
- Docker Desktop (debe estar abierto para usar la base de datos)

> **Nota sobre uv:** con el entorno `(recipe-api)` activo, `py -m uv ...` falla porque `py` usa el Python del `.venv`, que no tiene el módulo `uv`. Usa `uv ...` directamente. Fuera del entorno virtual, `py -m uv ...` sí funciona.

## Puesta en marcha rápida

Desde la carpeta `recipe-api`:

```powershell
# 1. Instalar dependencias y crear .venv
uv sync

# 2. Crear el archivo .env (ver sección "Configuración")

# 3. Levantar PostgreSQL
docker compose up -d --wait

# 4. Probar la conexión a la base de datos
uv run python scripts/test_connection.py

# 5. Crear las tablas (aplicar migraciones)
uv run alembic upgrade head

# 6. Iniciar la API
uv run uvicorn recipe_api.main:app --reload
```

La API queda disponible en <http://127.0.0.1:8000> y la documentación interactiva (Swagger) en <http://127.0.0.1:8000/docs>.

## Endpoints

| Método | Ruta | Descripción |
| --- | --- | --- |
| GET | `/` | Mensaje de bienvenida |
| GET | `/health` | Estado del servicio (`{"status": "UP"}`) |
| GET | `/api/v1/areas` | Listar áreas |
| GET | `/api/v1/areas/{id}` | Obtener un área (404 si no existe) |
| POST | `/api/v1/areas` | Crear un área (409 si el nombre ya existe) |
| PUT | `/api/v1/areas/{id}` | Actualizar un área (404 / 409) |
| DELETE | `/api/v1/areas/{id}` | Eliminar un área (204; 404 si no existe) |

Ejemplo de cuerpo para crear o actualizar un área:

```json
{ "name": "Peruana" }
```

## Configuración

Crea un archivo `.env` en la raíz de `recipe-api` (ya está en `.gitignore`, no se sube al repositorio):

```env
APP_NAME=Recipe API
APP_VERSION=1.0.0

# Cadena de conexión que usa la aplicación
DATABASE_URL=postgresql+psycopg://postgres:TU_PASSWORD@localhost:5432/recipes_db

# Credenciales con las que Docker crea la base de datos (deben coincidir con DATABASE_URL)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=TU_PASSWORD
POSTGRES_DB=recipes_db
```

Las variables se leen en [src/recipe_api/core/config.py](src/recipe_api/core/config.py) con `pydantic-settings`. Alembic usa esa misma `DATABASE_URL` (ver [migrations/env.py](migrations/env.py)), por lo que no hay que configurar `sqlalchemy.url` en `alembic.ini`.

## Base de datos con Docker

El archivo [docker-compose.yml](docker-compose.yml) define el servicio `db` (contenedor `recipe-db`, imagen `postgres:18`, puerto `5432`). Los datos se guardan en el volumen `recipe_pgdata` y sobreviven a reinicios.

```powershell
docker compose up -d --wait   # levantar y esperar a que esté sano
docker compose ps             # ver estado
docker compose logs -f db     # ver logs
docker compose down           # apagar (conserva los datos)
docker compose down -v        # apagar y BORRAR los datos
```

> **PostgreSQL 18:** el volumen se monta en `/var/lib/postgresql` (no en `/var/lib/postgresql/data`, como en versiones anteriores). Al cambiar de versión mayor con datos reales hay que usar `pg_dump` / `pg_upgrade`; el volumen de otra versión no se puede reutilizar tal cual.

### Probar la conexión

```powershell
uv run python scripts/test_connection.py
```

Salida esperada:

```text
Conexión exitosa a PostgreSQL
PostgreSQL 18.x (Debian ...) on x86_64-pc-linux-gnu ...
```

Si el script se queda esperando sin responder, normalmente no hay ningún PostgreSQL escuchando en `localhost:5432`: revisa que Docker Desktop esté abierto y que el contenedor esté `healthy` con `docker compose ps`.

## Migraciones con Alembic

Las migraciones viven en [migrations/versions/](migrations/versions/). Todos los comandos se ejecutan desde `recipe-api`.

```powershell
uv run alembic --version                                          # verificar instalación
uv run alembic revision --autogenerate -m "create areas table"    # generar migración desde los modelos
uv run alembic upgrade head                                       # aplicar todas las migraciones
uv run alembic downgrade -1                                       # revertir la última migración
uv run alembic current                                            # ver la versión aplicada
uv run alembic history                                            # ver el historial
```

Para que `--autogenerate` detecte una tabla nueva, importa su modelo en [migrations/env.py](migrations/env.py), junto a `Area`:

```python
from recipe_api.modules.areas.model import Area
from recipe_api.modules.categories.model import Category  # ejemplo
```

Revisa siempre el archivo generado en `migrations/versions/` antes de aplicarlo.

### Flujo para cada tabla nueva

Aplica cada migración **antes** de generar la siguiente; si no, Alembic falla con `Target database is not up to date`.

```powershell
uv run alembic revision --autogenerate -m "create units table"   # 1. generar
# 2. revisar el archivo creado en migrations/versions/
uv run alembic upgrade head                                      # 3. aplicar
uv run alembic check                                             # 4. verificar (debe decir "No new upgrade operations detected")
```

### Recrear la base desde cero (solo desarrollo)

Borra **todos los datos** del esquema `public` (incluida `alembic_version`) y vuelve a crear las tablas con las migraciones existentes:

```powershell
# 1. Eliminar todas las tablas dentro del contenedor
docker exec recipe-db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "DROP SCHEMA public CASCADE" -c "CREATE SCHEMA public"'

# 2. Recrear las tablas aplicando las migraciones
uv run alembic upgrade head

# 3. Verificar tablas y versión
docker exec recipe-db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\dt"'
uv run alembic current
uv run alembic check
```

Si la carpeta `migrations/versions/` está vacía o no coincide con lo que registra la base, genera primero una migración inicial con `uv run alembic revision --autogenerate -m "initial schema"` antes del paso 2. Revisa que no queden migraciones vacías (solo `pass`) y bórralas si aparecen.

Alternativa más drástica: `docker compose down -v` borra el volumen completo y `docker compose up -d --wait` crea una base nueva.

## Estructura del proyecto

```text
recipe-api/
├── docker-compose.yml
├── alembic.ini
├── pyproject.toml
├── uv.lock
├── .env                      # no versionado
├── migrations/               # Alembic
│   ├── env.py
│   └── versions/
├── scripts/
│   └── test_connection.py    # prueba de conexión a PostgreSQL
└── src/
    └── recipe_api/
        ├── main.py           # aplicación FastAPI y registro de routers
        ├── core/
        │   ├── config.py     # Settings (pydantic-settings)
        │   └── database.py   # engine, SessionLocal, Base, get_db
        ├── common/
        │   ├── exceptions.py # ResourceNotFoundError, ResourceAlreadyExistsError
        │   └── pagination.py
        └── modules/
            ├── areas/        # implementado
            ├── categories/   # pendiente
            ├── units/        # pendiente
            ├── ingredients/  # pendiente
            └── recipes/      # pendiente
```

Para ver el árbol en PowerShell: `tree src /F`

### Organización de cada módulo

Cada módulo en `modules/` sigue las mismas capas. Este es el orden recomendado para implementarlas:

| Orden | Archivo | Responsabilidad |
| --- | --- | --- |
| 1 | `model.py` | Representación de la tabla (SQLAlchemy) |
| 2 | `schemas.py` | Esquemas de request y response (Pydantic) |
| 3 | `repository.py` | Operaciones SQL / acceso a datos |
| 4 | `service.py` | Lógica de negocio y manejo de errores |
| 5 | `router.py` | Endpoints REST |

Pasos para añadir un módulo nuevo (por ejemplo `categories`):

1. Implementar las cinco capas anteriores, tomando `areas` como modelo.
2. Importar el modelo en [migrations/env.py](migrations/env.py).
3. Generar y aplicar la migración (`alembic revision --autogenerate` y `alembic upgrade head`).
4. Registrar el router en [main.py](src/recipe_api/main.py) con `app.include_router(..., prefix="/api/v1")`.

## Cómo se creó el proyecto (referencia)

### 1. Proyecto base

```powershell
uv init --package --name recipe-api --python 3.15
uv sync
```

`uv sync` busca una instalación compatible de Python 3.15, crea el entorno virtual `.venv`, resuelve las dependencias y genera `uv.lock`.

### 2. Dependencias

```powershell
uv add fastapi uvicorn
uv add sqlalchemy "psycopg[binary]" pydantic-settings
uv add alembic
```

Verificación:

```powershell
uv run python -c "import sqlalchemy, psycopg, pydantic_settings; print('Dependencias instaladas correctamente')"
```

### 3. Carpetas

```powershell
$base = "src/recipe_api"

$folders = @(
    "$base/core",
    "$base/common",
    "$base/modules",
    "$base/modules/areas",
    "$base/modules/categories",
    "$base/modules/units",
    "$base/modules/ingredients",
    "$base/modules/recipes"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path $folder -Force | Out-Null
}
```

`-Force` permite ejecutar el comando aunque algunas carpetas ya existan; `Out-Null` evita ruido en la terminal.

### 4. Archivos Python

```powershell
$base = "src/recipe_api"

$files = @(
    "$base/core/__init__.py",
    "$base/core/config.py",
    "$base/core/database.py",

    "$base/common/__init__.py",
    "$base/common/exceptions.py",
    "$base/common/pagination.py",

    "$base/modules/__init__.py"
)

$modules = @("areas", "categories", "units", "ingredients", "recipes")

foreach ($module in $modules) {
    $files += "$base/modules/$module/__init__.py"
    $files += "$base/modules/$module/router.py"
    $files += "$base/modules/$module/service.py"
    $files += "$base/modules/$module/repository.py"
    $files += "$base/modules/$module/model.py"
    $files += "$base/modules/$module/schemas.py"
}

foreach ($file in $files) {
    if (-not (Test-Path $file)) {
        New-Item -ItemType File -Path $file | Out-Null
    }
}
```

### 5. Alembic

```powershell
uv run alembic init migrations
```

Después se editó `migrations/env.py` para usar `settings.database_url` y `Base.metadata`.


------

mkdir src\recipe_api\modules\steps
ni src\recipe_api\modules\steps\__init__.py -ItemType File
ni src\recipe_api\modules\steps\model.py -ItemType File
ni src\recipe_api\modules\steps\schemas.py -ItemType File
ni src\recipe_api\modules\steps\repository.py -ItemType File
ni src\recipe_api\modules\steps\service.py -ItemType File
ni src\recipe_api\modules\steps\router.py -ItemType File


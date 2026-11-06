
from sqlalchemy import text

from recipe_api.core.database import engine

def main():
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT version()")
            )

            print("Conexión exitosa a PostgreSQL")
            print(result.scalar())

    except Exception as error:
        print("Error al conectar con PostgreSQL")
        print(error)
        raise


if __name__ == "__main__":
    main()

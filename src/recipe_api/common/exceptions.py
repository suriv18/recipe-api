class AppError(Exception):
    """Excepción base de la aplicación."""


class ResourceNotFoundError(AppError):
    """El recurso solicitado no existe."""


class ResourceAlreadyExistsError(AppError):
    """El recurso ya existe (nombre duplicado, etc.)."""

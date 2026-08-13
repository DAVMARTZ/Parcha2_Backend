class UserServiceError(Exception):
    """Error base de la lógica de negocio del módulo de usuarios."""


class DuplicateUserError(UserServiceError):
    """El uid de Firebase ya tiene un perfil registrado."""


class InvalidRoleError(UserServiceError):
    """El rol solicitado no es válido o no puede auto-registrarse."""


class UserNotFoundError(UserServiceError):
    """No existe un perfil para el uid consultado."""

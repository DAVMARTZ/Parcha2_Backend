from enum import Enum


class Role(str, Enum):
    """Roles de usuario del sistema.

    Los roles se almacenan como texto legible en la colección "users" de
    MongoDB. Heredar de ``str`` permite usarlos como valores JSON.
    """

    USER = "usuario"
    COMPANY = "empresa"
    ADMIN = "admin"

    @classmethod
    def values(cls):
        return [role.value for role in cls]

    @classmethod
    def public_registration_values(cls):
        """Roles permitidos en el registro público.

        El rol de administrador no puede auto-registrarse; se asigna de forma
        manual o mediante el comando de siembra ``seed_admin``.
        """
        return [cls.USER.value, cls.COMPANY.value]

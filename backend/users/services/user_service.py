from datetime import datetime, timezone

from users.exceptions import (
    DuplicateUserError,
    InvalidRoleError,
    UserNotFoundError,
)
from users.repositories.user_repository import UserRepository
from users.roles import Role


class UserService:
    """Lógica de negocio de los perfiles de usuario.

    Depende de un ``UserRepository`` mediante inyección de dependencias para
    facilitar las pruebas y mantener la separación de responsabilidades.
    """

    def __init__(self, repository=None):
        self.repository = repository if repository is not None else UserRepository()

    def register(self, uid, email, nombre, role):
        """Registra el perfil de un usuario ya autenticado en Firebase.

        Solo se permiten roles de registro público; el rol de administrador se
        asigna mediante ``create_admin`` o el comando ``seed_admin``.
        """
        if role not in Role.public_registration_values():
            raise InvalidRoleError(f"El rol '{role}' no puede auto-registrarse.")

        if self.repository.find_by_uid(uid):
            raise DuplicateUserError("Ya existe un perfil para este usuario.")

        document = {
            "uid": uid,
            "email": email,
            "nombre": nombre,
            "role": role,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        return self.repository.create(document)

    def create_admin(self, uid, email, nombre):
        """Crea o actualiza un perfil con rol administrador.

        Destinado a la siembra manual; los administradores no se auto-registran.
        """
        if self.repository.find_by_uid(uid):
            return self.update_role(uid, Role.ADMIN.value)

        document = {
            "uid": uid,
            "email": email,
            "nombre": nombre,
            "role": Role.ADMIN.value,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        return self.repository.create(document)

    def get_profile(self, uid):
        return self.repository.find_by_uid(uid)

    def list_profiles(self):
        return self.repository.find_all()

    def update_role(self, uid, role):
        if role not in Role.values():
            raise InvalidRoleError(f"Rol inválido: {role}.")

        profile = self.repository.update_role(uid, role)
        if profile is None:
            raise UserNotFoundError("No existe un perfil para este usuario.")
        return profile

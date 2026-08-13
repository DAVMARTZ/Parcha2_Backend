from rest_framework.permissions import BasePermission

from users.roles import Role
from users.services.user_service import UserService


class IsAdminUser(BasePermission):
    """Solo perfiles con rol ``admin`` pueden ejecutar la acción."""

    message = "Se requieren permisos de administrador."

    def has_permission(self, request, view):
        if not getattr(request.user, "is_authenticated", False):
            return False

        uid = request.firebase_user.get("uid")
        profile = UserService().get_profile(uid)
        return profile is not None and profile["role"] == Role.ADMIN.value

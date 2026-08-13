from rest_framework import serializers

from users.roles import Role


class RegisterUserSerializer(serializers.Serializer):
    """Datos mínimos para registrar el perfil del usuario autenticado."""

    nombre = serializers.CharField(min_length=2, max_length=120)
    role = serializers.ChoiceField(
        choices=[(value, value) for value in Role.public_registration_values()]
    )


class RoleUpdateSerializer(serializers.Serializer):
    """Permite a un administrador cambiar el rol de un perfil."""

    role = serializers.ChoiceField(choices=[(value, value) for value in Role.values()])


class UserProfileSerializer(serializers.Serializer):
    """Representación de un perfil de usuario en la API."""

    id = serializers.CharField()
    uid = serializers.CharField()
    email = serializers.EmailField()
    nombre = serializers.CharField()
    role = serializers.CharField()
    created_at = serializers.CharField()

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)

from users.exceptions import (
    DuplicateUserError,
    InvalidRoleError,
    UserNotFoundError,
)
from users.permissions import IsAdminUser
from users.serializers import (
    RegisterUserSerializer,
    RoleUpdateSerializer,
    UserProfileSerializer,
)
from users.services.user_service import UserService


class RegisterView(APIView):
    """Registra el perfil del usuario autenticado en Firebase.

    El usuario ya debe existir en Firebase Authentication (lo crea el frontend)
    y enviar un ID token vigente. El uid se obtiene del token, nunca del cuerpo.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Registrar perfil de usuario",
        description=(
            "Crea el perfil (nombre + rol) del usuario autenticado en la "
            "colección users. Roles permitidos: usuario o empresa."
        ),
        request=RegisterUserSerializer,
        responses={201: UserProfileSerializer},
    )
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = request.firebase_user["uid"]
        email = request.firebase_user.get("email")

        try:
            profile = UserService().register(
                uid=uid,
                email=email,
                nombre=serializer.validated_data["nombre"],
                role=serializer.validated_data["role"],
            )
        except DuplicateUserError:
            return Response(
                {"detail": "Ya existe un perfil para este usuario."},
                status=status.HTTP_409_CONFLICT,
            )
        except InvalidRoleError as exc:
            return Response(
                {"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            UserProfileSerializer(profile).data,
            status=status.HTTP_201_CREATED,
        )


class MeView(APIView):
    """Devuelve el perfil del usuario autenticado."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Obtener mi perfil",
        responses={200: UserProfileSerializer},
    )
    def get(self, request):
        profile = UserService().get_profile(request.firebase_user["uid"])

        if profile is None:
            return Response(
                {"detail": "Perfil no encontrado. Regístrese primero."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(UserProfileSerializer(profile).data)


@extend_schema_view(
    retrieve=extend_schema(
        parameters=[
            OpenApiParameter(
                "uid",
                OpenApiTypes.STR,
                description="UID del usuario en Firebase.",
            )
        ]
    ),
    update_role=extend_schema(
        parameters=[
            OpenApiParameter(
                "uid",
                OpenApiTypes.STR,
                description="UID del usuario en Firebase.",
            )
        ]
    ),
)
class UserViewSet(viewsets.ViewSet):
    """Administración de perfiles. Exclusiva para el rol admin."""

    permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = "uid"

    @extend_schema(
        summary="Listar perfiles",
        description="Devuelve todos los perfiles registrados. Solo admin.",
        responses={200: UserProfileSerializer(many=True)},
    )
    def list(self, request):
        profiles = UserService().list_profiles()
        return Response(UserProfileSerializer(profiles, many=True).data)

    @extend_schema(
        summary="Obtener perfil por uid",
        responses={200: UserProfileSerializer},
    )
    def retrieve(self, request, uid=None):
        profile = UserService().get_profile(uid)

        if profile is None:
            return Response(
                {"detail": "Usuario no encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(UserProfileSerializer(profile).data)

    @extend_schema(
        summary="Cambiar rol de un perfil",
        request=RoleUpdateSerializer,
        responses={200: UserProfileSerializer},
    )
    @action(detail=True, methods=["patch"], url_path="role")
    def update_role(self, request, uid=None):
        serializer = RoleUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            profile = UserService().update_role(
                uid, serializer.validated_data["role"]
            )
        except UserNotFoundError:
            return Response(
                {"detail": "Usuario no encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(UserProfileSerializer(profile).data)

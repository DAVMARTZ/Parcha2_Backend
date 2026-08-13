from django.core.management.base import BaseCommand

from users.roles import Role
from users.services.user_service import UserService


class Command(BaseCommand):
    """Crea o actualiza un perfil de administrador en MongoDB.

    Los administradores no se auto-registran; este comando es la vía manual
    para asignar el rol admin a un usuario de Firebase existente.
    """

    help = "Crea o actualiza un perfil de administrador en MongoDB"

    def add_arguments(self, parser):
        parser.add_argument("--uid", required=True, help="UID del usuario en Firebase.")
        parser.add_argument("--email", required=True, help="Correo del administrador.")
        parser.add_argument(
            "--nombre", default="Administrador", help="Nombre del administrador."
        )

    def handle(self, *args, **options):
        service = UserService()
        existing = service.get_profile(options["uid"])

        if existing:
            service.update_role(options["uid"], Role.ADMIN.value)
            message = f"Rol actualizado a '{Role.ADMIN.value}' para uid {options['uid']}."
        else:
            service.create_admin(
                uid=options["uid"],
                email=options["email"],
                nombre=options["nombre"],
            )
            message = f"Perfil de administrador creado para {options['email']}."

        self.stdout.write(self.style.SUCCESS(message))

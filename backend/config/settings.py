from pathlib import Path
from dotenv import load_dotenv
import os

# Identifica la carpeta raíz del backend.
BASE_DIR = Path(__file__).resolve().parent.parent

# Carga las variables del archivo .env para que puedan leerse con os.getenv().
load_dotenv(BASE_DIR / ".env")

# Obtiene la clave secreta usada por Django desde variables de entorno.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# Convierte el valor de entorno en un booleano para activar o desactivar el modo debug.
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

# Convierte la lista de hosts permitidos en una lista Python separada por comas.
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Registra las aplicaciones instaladas en el proyecto.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "companies",
    "users",
]

# Define la cadena de middlewares que procesa cada solicitud HTTP.
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
# En este taller, TEMPLATES se mantiene en settings.py porque Django lo necesita
# para componentes internos como el panel de administración. Esta configuración
# se usa cuando el backend debe renderizar HTML desde el servidor, aunque el foco
# principal del proyecto sea exponer una API REST.



TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Indica a Django dónde está el archivo principal de rutas.
ROOT_URLCONF = "config.urls"

# Define el punto de entrada WSGI del proyecto.
WSGI_APPLICATION = "config.wsgi.application"

# Lee los orígenes permitidos para las peticiones del frontend.
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:5173").split(",")

# Configuración base de Django REST Framework.
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "companies.firebase_auth.FirebaseAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Configuración de drf-spectacular (Swagger / OpenAPI).
SPECTACULAR_SETTINGS = {
    "TITLE": "Eco-Red API",
    "DESCRIPTION": (
        "Microservicio de autenticación y gestión de empresas y publicaciones "
        "de materiales reciclables. Autenticación mediante tokens de Firebase."
    ),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SECURITY": [{"BearerAuth": []}],
    "SECURITY_SCHEMES": {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": (
                "ID token de Firebase. Se obtiene iniciando sesión en "
                "Firebase (Authentication). Pegarlo en el botón Authorize."
            ),
        }
    },
}

# Configuración general de idioma y zona horaria.
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

# Configuración de archivos estáticos.
STATIC_URL = "static/"

# Tipo de llave primaria por defecto para modelos Django.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configuración mínima de logs hacia consola.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
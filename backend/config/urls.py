from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from companies.views import CompanyViewSet, MaterialListingViewSet, health

# Crea un router para registrar rutas REST automáticamente.
router = DefaultRouter()

# Registra las rutas de empresas.
router.register(r"companies", CompanyViewSet, basename="companies")

# Registra las rutas de publicaciones de materiales.
router.register(r"material-listings", MaterialListingViewSet, basename="material-listings")

# Expone las rutas públicas de la app.
urlpatterns = [
    path("health/", health),
    path("", include(router.urls)),
]

# Define las rutas principales del proyecto.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("companies.urls")),
]
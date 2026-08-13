from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CompanyViewSet, MaterialListingViewSet, health

# Crea un router para registrar rutas REST automáticamente.
router = DefaultRouter()

# Registra las rutas de empresas.
router.register(r"companies", CompanyViewSet, basename="companies")

# Registra las rutas de publicaciones de materiales.
router.register(r"materials", MaterialListingViewSet, basename="materials")

# Expone las rutas públicas de la app.
urlpatterns = [
    path("health/", health),
    path("", include(router.urls)),
]
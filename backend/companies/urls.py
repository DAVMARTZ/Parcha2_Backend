from rest_framework.routers import DefaultRouter
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

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
    # Documentación OpenAPI y Swagger UI.
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("", include(router.urls)),
]
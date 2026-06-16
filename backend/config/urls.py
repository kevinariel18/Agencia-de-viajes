from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path("django-admin/", admin.site.urls),

    # Auth: login, logout, register
    path("auth/", include("apps.accounts.urls")),

    # Root: redirect según rol
    path("", include("apps.accounts.urls_root")),

    # ── Panel Administrador ─────────────────────────────────────
    # Cada módulo admin tiene su propio app_name namespace
    path("administracion/", include("apps.reports.urls_admin")),      # admin_panel
    path("administracion/", include("apps.accounts.urls_admin")),     #co admin_users
    path("administracion/", include("apps.locations.urls_admin")),    # locations
    path("administracion/", include("apps.destinations.urls_admin")), # destinations
    path("administracion/", include("apps.packages.urls_admin")),     # packages
    path("administracion/", include("apps.reservations.urls_admin")), # reservations

    # ── Área Cliente ────────────────────────────────────────────
    # Un solo archivo con app_name="client" centraliza todo
    path("cliente/", include("config.urls_client")),

    # ── REST API ────────────────────────────────────────────────
    path("api/", include("config.api_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

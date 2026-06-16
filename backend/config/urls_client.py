"""
URLs unificadas para el área de cliente.
app_name="client" es el único namespace del área de cliente.
"""
from django.urls import path
from apps.packages.views import ClientPackageListView, ClientPackageDetailView
from apps.reservations.views import (
    ClientReservationListView,
    ClientReservationDetailView,
    client_create_reservation,
    client_cancel_reservation,
)
from apps.accounts.views import profile_view, change_password_view

app_name = "client"

urlpatterns = [
    # ── Paquetes ─────────────────────────────────────────────
    path("paquetes/", ClientPackageListView.as_view(), name="package_list"),
    path("paquetes/<int:pk>/", ClientPackageDetailView.as_view(), name="package_detail"),

    # ── Reservas (nueva ANTES que detalle para evitar colisión) ──
    path("reservas/", ClientReservationListView.as_view(), name="reservation_list"),
    path("reservas/nueva/<int:departure_pk>/", client_create_reservation, name="reservation_create"),
    path("reservas/<int:pk>/cancelar/", client_cancel_reservation, name="reservation_cancel"),
    path("reservas/<int:pk>/", ClientReservationDetailView.as_view(), name="reservation_detail"),

    # ── Perfil ────────────────────────────────────────────────
    path("perfil/", profile_view, name="profile"),
    path("cambiar-contrasena/", change_password_view, name="change_password"),
]

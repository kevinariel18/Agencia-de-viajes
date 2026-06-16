from django.urls import path
from . import views

app_name = "reservations"

urlpatterns = [
    path("reservas/", views.AdminReservationListView.as_view(), name="admin_list"),
    path("reservas/<int:pk>/", views.AdminReservationDetailView.as_view(), name="admin_detail"),
    path("reservas/<int:pk>/confirmar/", views.admin_confirm_reservation, name="admin_confirm"),
    path("reservas/<int:pk>/cancelar/", views.admin_cancel_reservation, name="admin_cancel"),
]

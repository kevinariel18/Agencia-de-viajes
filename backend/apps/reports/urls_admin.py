from django.urls import path
from .views import DashboardView, ReportsView

app_name = "admin_panel"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("reportes/", ReportsView.as_view(), name="reports"),
]

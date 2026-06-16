from django.urls import path
from .views import UserListView

app_name = "admin_users"

urlpatterns = [
    path("usuarios/", UserListView.as_view(), name="list"),
]

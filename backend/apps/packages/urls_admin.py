from django.urls import path
from . import views

app_name = "packages"

urlpatterns = [
    path("paquetes/", views.PackageListView.as_view(), name="list"),
    path("paquetes/nuevo/", views.PackageCreateView.as_view(), name="create"),
    path("paquetes/<int:pk>/editar/", views.PackageUpdateView.as_view(), name="update"),
    path("paquetes/<int:pk>/detalle/", views.PackageDetailAdminView.as_view(), name="admin_detail"),
    path("paquetes/<int:pk>/toggle/", views.package_toggle, name="toggle"),
    path("paquetes/<int:pkg_pk>/destinos/agregar/", views.PackageDestinationCreateView.as_view(), name="add_destination"),
    path("paquetes/<int:pkg_pk>/destinos/<int:pk>/eliminar/", views.package_destination_remove, name="remove_destination"),
    path("salidas/", views.DepartureListView.as_view(), name="departure_list"),
    path("salidas/nueva/", views.DepartureCreateView.as_view(), name="departure_create"),
    path("salidas/<int:pk>/editar/", views.DepartureUpdateView.as_view(), name="departure_update"),
]

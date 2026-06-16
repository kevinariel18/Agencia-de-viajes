from django.urls import path
from . import views

app_name = "destinations"

urlpatterns = [
    path("destinos/", views.DestinationListView.as_view(), name="list"),
    path("destinos/nuevo/", views.DestinationCreateView.as_view(), name="create"),
    path("destinos/<int:pk>/editar/", views.DestinationUpdateView.as_view(), name="update"),
    path("destinos/<int:pk>/detalle/", views.DestinationDetailView.as_view(), name="detail"),
    path("destinos/<int:pk>/toggle/", views.destination_toggle, name="toggle"),
]

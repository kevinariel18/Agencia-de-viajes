from django.urls import path
from . import views

app_name = "locations"

urlpatterns = [
    path("paises/", views.CountryListView.as_view(), name="country_list"),
    path("paises/nuevo/", views.CountryCreateView.as_view(), name="country_create"),
    path("paises/<int:pk>/editar/", views.CountryUpdateView.as_view(), name="country_update"),
    path("paises/<int:pk>/toggle/", views.country_toggle, name="country_toggle"),
    path("ciudades/", views.CityListView.as_view(), name="city_list"),
    path("ciudades/nueva/", views.CityCreateView.as_view(), name="city_create"),
    path("ciudades/<int:pk>/editar/", views.CityUpdateView.as_view(), name="city_update"),
    path("ciudades/<int:pk>/toggle/", views.city_toggle, name="city_toggle"),
]

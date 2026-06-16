from django.urls import path
from .views import root_redirect

urlpatterns = [
    path("", root_redirect, name="home"),
]

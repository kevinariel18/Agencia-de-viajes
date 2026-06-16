from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not request.user.is_admin_role():
            return HttpResponseForbidden("Acceso denegado.")
        return view_func(request, *args, **kwargs)
    return wrapper


def client_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not request.user.is_client_role():
            return HttpResponseForbidden("Acceso denegado.")
        return view_func(request, *args, **kwargs)
    return wrapper


class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not request.user.is_admin_role():
            return HttpResponseForbidden("Acceso denegado.")
        return super().dispatch(request, *args, **kwargs)


class ClientRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not request.user.is_client_role():
            return HttpResponseForbidden("Acceso denegado.")
        return super().dispatch(request, *args, **kwargs)

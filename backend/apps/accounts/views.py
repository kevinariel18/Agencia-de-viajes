from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from .forms import LoginForm, ClientRegisterForm, UserProfileForm, CustomPasswordChangeForm
from .models import User
from .decorators import AdminRequiredMixin


def login_view(request):
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.status == User.Status.ACTIVE:
                login(request, user)
                return _redirect_by_role(user)
            messages.error(request, "Tu cuenta está inactiva o suspendida.")
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


def register_view(request):
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)
    if request.method == "POST":
        form = ClientRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cuenta creada. ¡Bienvenido!")
            return redirect("client:package_list")
        messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = ClientRegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def profile_view(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado.")
            return redirect("client:profile")
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, "client/profile.html", {"form": form})


@login_required
def change_password_view(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Contraseña actualizada.")
            return redirect("client:profile")
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, "client/change_password.html", {"form": form})


def root_redirect(request):
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)
    return redirect("login")


def _redirect_by_role(user):
    if user.is_admin_role():
        return redirect("admin_panel:dashboard")
    return redirect("client:package_list")


class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = "admin_panel/users/list.html"
    context_object_name = "users"
    paginate_by = 15

    def get_queryset(self):
        qs = User.objects.select_related("city__country").order_by("-created_at")
        q = self.request.GET.get("q", "")
        role = self.request.GET.get("role", "")
        if q:
            qs = qs.filter(email__icontains=q) | qs.filter(
                first_name__icontains=q) | qs.filter(last_name__icontains=q)
        if role:
            qs = qs.filter(role=role)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["roles"] = User.Role.choices
        return ctx

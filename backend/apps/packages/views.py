from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import TourPackage, PackageDestination, Departure
from .forms import TourPackageForm, PackageDestinationForm, DepartureForm, PackageFilterForm
from apps.accounts.decorators import AdminRequiredMixin, ClientRequiredMixin


# ── Admin ─────────────────────────────────────────────────────────────────────

class PackageListView(AdminRequiredMixin, ListView):
    model = TourPackage
    template_name = "admin_panel/packages/list.html"
    context_object_name = "packages"
    paginate_by = 15

    def get_queryset(self):
        qs = TourPackage.objects.prefetch_related("package_destinations__destination")
        q = self.request.GET.get("q", "")
        category = self.request.GET.get("category", "")
        if q:
            qs = qs.filter(name__icontains=q)
        if category:
            qs = qs.filter(category=category)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = TourPackage.Category.choices
        return ctx


class PackageCreateView(AdminRequiredMixin, CreateView):
    model = TourPackage
    form_class = TourPackageForm
    template_name = "admin_panel/packages/form.html"
    success_url = reverse_lazy("packages:list")

    def form_valid(self, form):
        messages.success(self.request, "Paquete registrado correctamente.")
        return super().form_valid(form)


class PackageUpdateView(AdminRequiredMixin, UpdateView):
    model = TourPackage
    form_class = TourPackageForm
    template_name = "admin_panel/packages/form.html"
    success_url = reverse_lazy("packages:list")

    def form_valid(self, form):
        messages.success(self.request, "Paquete actualizado correctamente.")
        return super().form_valid(form)


class PackageDetailAdminView(AdminRequiredMixin, DetailView):
    model = TourPackage
    template_name = "admin_panel/packages/detail.html"
    context_object_name = "package"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["departures"] = self.object.departures.all()
        ctx["pkg_destinations"] = self.object.package_destinations.select_related(
            "destination__city"
        ).all()
        return ctx


def package_toggle(request, pk):
    if not request.user.is_authenticated or not request.user.is_admin_role():
        return HttpResponseForbidden()
    pkg = get_object_or_404(TourPackage, pk=pk)
    pkg.is_active = not pkg.is_active
    pkg.save()
    messages.success(request, f"Paquete {'activado' if pkg.is_active else 'desactivado'}.")
    return redirect("packages:list")


class PackageDestinationCreateView(AdminRequiredMixin, CreateView):
    model = PackageDestination
    form_class = PackageDestinationForm
    template_name = "admin_panel/packages/destination_form.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["package"] = get_object_or_404(TourPackage, pk=self.kwargs["pkg_pk"])
        return ctx

    def form_valid(self, form):
        form.instance.package_id = self.kwargs["pkg_pk"]
        messages.success(self.request, "Destino asociado al paquete.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("packages:admin_detail", kwargs={"pk": self.kwargs["pkg_pk"]})


def package_destination_remove(request, pkg_pk, pk):
    if not request.user.is_authenticated or not request.user.is_admin_role():
        return HttpResponseForbidden()
    pd = get_object_or_404(PackageDestination, pk=pk, package_id=pkg_pk)
    pd.delete()
    messages.success(request, "Destino eliminado del paquete.")
    return redirect("packages:admin_detail", pk=pkg_pk)


# ── Departures ────────────────────────────────────────────────────────────────

class DepartureListView(AdminRequiredMixin, ListView):
    model = Departure
    template_name = "admin_panel/packages/departure_list.html"
    context_object_name = "departures"
    paginate_by = 20

    def get_queryset(self):
        return Departure.objects.select_related("package").order_by("departure_date")


class DepartureCreateView(AdminRequiredMixin, CreateView):
    model = Departure
    form_class = DepartureForm
    template_name = "admin_panel/packages/departure_form.html"
    success_url = reverse_lazy("packages:departure_list")

    def form_valid(self, form):
        messages.success(self.request, "Fecha de salida registrada.")
        return super().form_valid(form)


class DepartureUpdateView(AdminRequiredMixin, UpdateView):
    model = Departure
    form_class = DepartureForm
    template_name = "admin_panel/packages/departure_form.html"
    success_url = reverse_lazy("packages:departure_list")

    def form_valid(self, form):
        messages.success(self.request, "Fecha de salida actualizada.")
        return super().form_valid(form)


# ── Cliente ───────────────────────────────────────────────────────────────────

class ClientPackageListView(ClientRequiredMixin, ListView):
    model = TourPackage
    template_name = "client/packages/list.html"
    context_object_name = "packages"
    paginate_by = 12

    def get_queryset(self):
        qs = TourPackage.objects.filter(is_active=True).prefetch_related(
            "package_destinations__destination__city__country", "departures"
        )
        form = PackageFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get("q"):
                qs = qs.filter(name__icontains=form.cleaned_data["q"])
            if form.cleaned_data.get("category"):
                qs = qs.filter(category=form.cleaned_data["category"])
            if form.cleaned_data.get("price_min"):
                qs = qs.filter(price__gte=form.cleaned_data["price_min"])
            if form.cleaned_data.get("price_max"):
                qs = qs.filter(price__lte=form.cleaned_data["price_max"])
            if form.cleaned_data.get("days"):
                qs = qs.filter(days=form.cleaned_data["days"])
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filter_form"] = PackageFilterForm(self.request.GET)
        return ctx


class ClientPackageDetailView(ClientRequiredMixin, DetailView):
    model = TourPackage
    template_name = "client/packages/detail.html"
    context_object_name = "package"
    queryset = TourPackage.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        from django.utils import timezone
        ctx = super().get_context_data(**kwargs)
        ctx["departures"] = self.object.departures.filter(
            status="AVAILABLE",
            departure_date__gte=timezone.now().date(),
        ).order_by("departure_date")
        ctx["pkg_destinations"] = self.object.package_destinations.select_related(
            "destination__city__country"
        ).all()
        return ctx

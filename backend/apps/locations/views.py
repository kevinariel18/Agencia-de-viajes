from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from .models import Country, City
from .forms import CountryForm, CityForm
from apps.accounts.decorators import AdminRequiredMixin


class CountryListView(AdminRequiredMixin, ListView):
    model = Country
    template_name = "admin_panel/locations/country_list.html"
    context_object_name = "countries"
    paginate_by = 15

    def get_queryset(self):
        qs = Country.objects.all()
        q = self.request.GET.get("q", "")
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(code__icontains=q)
        return qs


class CountryCreateView(AdminRequiredMixin, CreateView):
    model = Country
    form_class = CountryForm
    template_name = "admin_panel/locations/country_form.html"
    success_url = reverse_lazy("locations:country_list")

    def form_valid(self, form):
        messages.success(self.request, "País registrado correctamente.")
        return super().form_valid(form)


class CountryUpdateView(AdminRequiredMixin, UpdateView):
    model = Country
    form_class = CountryForm
    template_name = "admin_panel/locations/country_form.html"
    success_url = reverse_lazy("locations:country_list")

    def form_valid(self, form):
        messages.success(self.request, "País actualizado correctamente.")
        return super().form_valid(form)


def country_toggle(request, pk):
    if not request.user.is_authenticated or not request.user.is_admin_role():
        return HttpResponseForbidden()
    country = get_object_or_404(Country, pk=pk)
    country.is_active = not country.is_active
    country.save()
    messages.success(request, f"País {'activado' if country.is_active else 'desactivado'}.")
    return redirect("locations:country_list")


class CityListView(AdminRequiredMixin, ListView):
    model = City
    template_name = "admin_panel/locations/city_list.html"
    context_object_name = "cities"
    paginate_by = 15

    def get_queryset(self):
        qs = City.objects.select_related("country")
        q = self.request.GET.get("q", "")
        country_id = self.request.GET.get("country", "")
        if q:
            qs = qs.filter(name__icontains=q)
        if country_id:
            qs = qs.filter(country_id=country_id)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["countries"] = Country.objects.filter(is_active=True)
        return ctx


class CityCreateView(AdminRequiredMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = "admin_panel/locations/city_form.html"
    success_url = reverse_lazy("locations:city_list")

    def form_valid(self, form):
        messages.success(self.request, "Ciudad registrada correctamente.")
        return super().form_valid(form)


class CityUpdateView(AdminRequiredMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = "admin_panel/locations/city_form.html"
    success_url = reverse_lazy("locations:city_list")

    def form_valid(self, form):
        messages.success(self.request, "Ciudad actualizada correctamente.")
        return super().form_valid(form)


def city_toggle(request, pk):
    if not request.user.is_authenticated or not request.user.is_admin_role():
        return HttpResponseForbidden()
    city = get_object_or_404(City, pk=pk)
    city.is_active = not city.is_active
    city.save()
    messages.success(request, f"Ciudad {'activada' if city.is_active else 'desactivada'}.")
    return redirect("locations:city_list")

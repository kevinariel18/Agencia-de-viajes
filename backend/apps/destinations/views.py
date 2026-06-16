from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Destination
from .forms import DestinationForm
from apps.accounts.decorators import AdminRequiredMixin
from apps.locations.models import Country, City


class DestinationListView(AdminRequiredMixin, ListView):
    model = Destination
    template_name = "admin_panel/destinations/list.html"
    context_object_name = "destinations"
    paginate_by = 15

    def get_queryset(self):
        qs = Destination.objects.select_related("city__country")
        q = self.request.GET.get("q", "")
        country_id = self.request.GET.get("country", "")
        city_id = self.request.GET.get("city", "")
        difficulty = self.request.GET.get("difficulty", "")
        if q:
            qs = qs.filter(name__icontains=q)
        if country_id:
            qs = qs.filter(city__country_id=country_id)
        if city_id:
            qs = qs.filter(city_id=city_id)
        if difficulty:
            qs = qs.filter(difficulty=difficulty)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["countries"] = Country.objects.filter(is_active=True)
        ctx["cities"] = City.objects.filter(is_active=True)
        ctx["difficulties"] = Destination.Difficulty.choices
        return ctx


class DestinationCreateView(AdminRequiredMixin, CreateView):
    model = Destination
    form_class = DestinationForm
    template_name = "admin_panel/destinations/form.html"
    success_url = reverse_lazy("destinations:list")

    def form_valid(self, form):
        messages.success(self.request, "Destino registrado correctamente.")
        return super().form_valid(form)


class DestinationUpdateView(AdminRequiredMixin, UpdateView):
    model = Destination
    form_class = DestinationForm
    template_name = "admin_panel/destinations/form.html"
    success_url = reverse_lazy("destinations:list")

    def form_valid(self, form):
        messages.success(self.request, "Destino actualizado correctamente.")
        return super().form_valid(form)


class DestinationDetailView(AdminRequiredMixin, DetailView):
    model = Destination
    template_name = "admin_panel/destinations/detail.html"
    context_object_name = "destination"


def destination_toggle(request, pk):
    if not request.user.is_authenticated or not request.user.is_admin_role():
        return HttpResponseForbidden()
    dest = get_object_or_404(Destination, pk=pk)
    dest.is_active = not dest.is_active
    dest.save()
    messages.success(request, f"Destino {'activado' if dest.is_active else 'desactivado'}.")
    return redirect("destinations:list")

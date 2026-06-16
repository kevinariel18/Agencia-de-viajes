from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.core.exceptions import ValidationError
from .models import Reservation
from .forms import ReservationCreateForm, ReservationFilterForm
from .services import create_reservation, confirm_reservation, cancel_reservation
from apps.accounts.decorators import AdminRequiredMixin, ClientRequiredMixin
from apps.packages.models import Departure


# ── Cliente ───────────────────────────────────────────────────────────────────

class ClientReservationListView(ClientRequiredMixin, ListView):
    model = Reservation
    template_name = "client/reservations/list.html"
    context_object_name = "reservations"
    paginate_by = 10

    def get_queryset(self):
        return Reservation.objects.filter(
            user=self.request.user
        ).select_related("departure__package").order_by("-created_at")


class ClientReservationDetailView(ClientRequiredMixin, DetailView):
    model = Reservation
    template_name = "client/reservations/detail.html"
    context_object_name = "reservation"

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


def client_create_reservation(request, departure_pk):
    if not request.user.is_authenticated or not request.user.is_client_role():
        return redirect("login")
    departure = get_object_or_404(Departure, pk=departure_pk, status="AVAILABLE")
    package = departure.package

    if request.method == "POST":
        form = ReservationCreateForm(request.POST)
        if form.is_valid():
            try:
                reservation = create_reservation(
                    user=request.user,
                    departure_id=departure.pk,
                    number_of_people=form.cleaned_data["number_of_people"],
                )
                messages.success(request, f"Reserva {reservation.public_code} creada exitosamente.")
                return redirect("client:reservation_detail", pk=reservation.pk)
            except ValidationError as e:
                messages.error(request, str(e.message))
        else:
            messages.error(request, "Por favor corrige los errores.")
    else:
        form = ReservationCreateForm(initial={"departure_id": departure.pk})

    return render(request, "client/reservations/create.html", {
        "form": form,
        "departure": departure,
        "package": package,
    })


def client_cancel_reservation(request, pk):
    if not request.user.is_authenticated or not request.user.is_client_role():
        return redirect("login")
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if reservation.status not in (Reservation.Status.PENDING,):
        messages.error(request, "No puedes cancelar esta reserva en su estado actual.")
        return redirect("client:reservation_list")
    if request.method == "POST":
        try:
            cancel_reservation(reservation.pk)
            messages.success(request, "Reserva cancelada correctamente.")
        except ValidationError as e:
            messages.error(request, str(e.message))
    return redirect("client:reservation_list")


# ── Administrador ─────────────────────────────────────────────────────────────

class AdminReservationListView(AdminRequiredMixin, ListView):
    model = Reservation
    template_name = "admin_panel/reservations/list.html"
    context_object_name = "reservations"
    paginate_by = 15

    def get_queryset(self):
        qs = Reservation.objects.select_related(
            "user", "departure__package"
        ).order_by("-created_at")
        form = ReservationFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get("status"):
                qs = qs.filter(status=form.cleaned_data["status"])
            if form.cleaned_data.get("q"):
                q = form.cleaned_data["q"]
                qs = qs.filter(public_code__icontains=q) | qs.filter(
                    user__email__icontains=q
                )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filter_form"] = ReservationFilterForm(self.request.GET)
        return ctx


class AdminReservationDetailView(AdminRequiredMixin, DetailView):
    model = Reservation
    template_name = "admin_panel/reservations/detail.html"
    context_object_name = "reservation"


def admin_confirm_reservation(request, pk):
    if not request.user.is_authenticated or not request.user.is_admin_role():
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()
    if request.method == "POST":
        try:
            confirm_reservation(pk)
            messages.success(request, "Reserva confirmada correctamente.")
        except ValidationError as e:
            messages.error(request, str(e.message))
    return redirect("reservations:admin_detail", pk=pk)


def admin_cancel_reservation(request, pk):
    if not request.user.is_authenticated or not request.user.is_admin_role():
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()
    if request.method == "POST":
        try:
            cancel_reservation(pk, cancelled_by_admin=True)
            messages.success(request, "Reserva cancelada y cupos devueltos.")
        except ValidationError as e:
            messages.error(request, str(e.message))
    return redirect("reservations:admin_list")

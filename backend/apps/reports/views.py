from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Sum, F, Q
from django.db.models.functions import Cast, ExtractYear, ExtractMonth
from django.db.models import DateField
from apps.accounts.decorators import AdminRequiredMixin
from apps.accounts.models import User
from apps.packages.models import TourPackage, Departure
from apps.reservations.models import Reservation
from django.views import View
import datetime


class DashboardView(AdminRequiredMixin, View):
    template_name = "admin_panel/dashboard.html"

    def get(self, request):
        now = timezone.now()

        total_users = User.objects.count()
        active_clients = User.objects.filter(role=User.Role.CLIENT, status=User.Status.ACTIVE).count()

        total_packages = TourPackage.objects.count()
        active_packages = TourPackage.objects.filter(is_active=True).count()

        pending_reservations = Reservation.objects.filter(status=Reservation.Status.PENDING).count()
        confirmed_reservations = Reservation.objects.filter(status=Reservation.Status.CONFIRMED).count()
        cancelled_reservations = Reservation.objects.filter(status=Reservation.Status.CANCELLED).count()

        total_revenue = Reservation.objects.filter(
            status=Reservation.Status.CONFIRMED
        ).aggregate(total=Sum("total_amount"))["total"] or 0

        upcoming_departures = Departure.objects.filter(
            departure_date__gte=now.date(),
            departure_date__lte=(now + timezone.timedelta(days=30)).date(),
            status=Departure.Status.AVAILABLE,
        ).select_related("package").order_by("departure_date")[:5]

        top_packages = TourPackage.objects.annotate(
            total_reservations=Count("departures__reservations")
        ).order_by("-total_reservations")[:5]

        package_occupancy = Departure.objects.filter(
            status__in=[Departure.Status.AVAILABLE, Departure.Status.FULL]
        ).select_related("package").annotate(
            occupancy=F("capacity") - F("available_slots")
        ).order_by("-occupancy")[:8]

        latest_reservations = Reservation.objects.select_related(
            "user", "departure__package"
        ).order_by("-created_at")[:10]

        context = {
            "total_users": total_users,
            "active_clients": active_clients,
            "total_packages": total_packages,
            "active_packages": active_packages,
            "pending_reservations": pending_reservations,
            "confirmed_reservations": confirmed_reservations,
            "cancelled_reservations": cancelled_reservations,
            "total_revenue": total_revenue,
            "upcoming_departures": upcoming_departures,
            "top_packages": top_packages,
            "package_occupancy": package_occupancy,
            "latest_reservations": latest_reservations,
        }
        return render(request, self.template_name, context)


class ReportsView(AdminRequiredMixin, View):
    template_name = "admin_panel/reports/index.html"

    def get(self, request):
        fecha_desde = request.GET.get("fecha_desde", "")
        fecha_hasta = request.GET.get("fecha_hasta", "")

        base_qs = Reservation.objects.all()
        if fecha_desde:
            dt_desde = datetime.datetime.strptime(fecha_desde, "%Y-%m-%d")
            dt_desde = dt_desde.replace(tzinfo=datetime.timezone.utc)
            base_qs = base_qs.filter(reservation_date__gte=dt_desde)
        if fecha_hasta:
            dt_hasta = datetime.datetime.strptime(fecha_hasta, "%Y-%m-%d")
            dt_hasta = dt_hasta.replace(hour=23, minute=59, second=59, tzinfo=datetime.timezone.utc)
            base_qs = base_qs.filter(reservation_date__lte=dt_hasta)

        by_status = base_qs.values("status").annotate(total=Count("id"))
        STATUS_LABELS = dict(Reservation.Status.choices)
        for item in by_status:
            item["status_display"] = STATUS_LABELS.get(item["status"], item["status"])

        revenue_by_package = base_qs.filter(
            status=Reservation.Status.CONFIRMED
        ).values(
            pkg_name=F("departure__package__name")
        ).annotate(revenue=Sum("total_amount")).order_by("-revenue")[:10]

        monthly = (
            base_qs.annotate(
                fecha=Cast("reservation_date", DateField()),
                year=ExtractYear("fecha"),
                month_num=ExtractMonth("fecha"),
            )
            .values("year", "month_num")
            .annotate(total=Count("id"))
            .filter(year__isnull=False, month_num__isnull=False)
            .order_by("-year", "-month_num")[:6]
        )
        MESES = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        for item in monthly:
            item["month_display"] = f"{MESES[item['month_num']]} {item['year']}"

        packages_sold = (
            base_qs.values(pkg_name=F("departure__package__name"))
            .annotate(total=Count("id"), revenue=Sum("total_amount"))
            .order_by("-total")
        )

        top_countries = (
            base_qs.values(
                country_name=F("departure__package__package_destinations__destination__city__country__name"),
                country_code=F("departure__package__package_destinations__destination__city__country__code"),
            )
            .annotate(total=Count("id", distinct=True))
            .order_by("-total")
        )

        top_cities = (
            base_qs.values(
                city_name=F("departure__package__package_destinations__destination__city__name"),
                country_name=F("departure__package__package_destinations__destination__city__country__name"),
            )
            .annotate(total=Count("id", distinct=True))
            .order_by("-total")
        )

        context = {
            "by_status": list(by_status),
            "revenue_by_package": list(revenue_by_package),
            "monthly": list(monthly),
            "packages_sold": list(packages_sold),
            "top_countries": list(top_countries),
            "top_cities": list(top_cities),
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
            "total_reservations": base_qs.count(),
        }
        return render(request, self.template_name, context)

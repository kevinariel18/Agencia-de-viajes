from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Sum, F
from apps.accounts.decorators import AdminRequiredMixin
from apps.accounts.models import User
from apps.packages.models import TourPackage, Departure
from apps.reservations.models import Reservation
from django.views import View


class DashboardView(AdminRequiredMixin, View):
    template_name = "admin_panel/dashboard.html"

    def get(self, request):
        now = timezone.now()

        # User stats
        total_users = User.objects.count()
        active_clients = User.objects.filter(role=User.Role.CLIENT, status=User.Status.ACTIVE).count()

        # Package stats
        total_packages = TourPackage.objects.count()
        active_packages = TourPackage.objects.filter(is_active=True).count()

        # Reservation stats
        pending_reservations = Reservation.objects.filter(status=Reservation.Status.PENDING).count()
        confirmed_reservations = Reservation.objects.filter(status=Reservation.Status.CONFIRMED).count()
        cancelled_reservations = Reservation.objects.filter(status=Reservation.Status.CANCELLED).count()

        # Revenue
        total_revenue = Reservation.objects.filter(
            status=Reservation.Status.CONFIRMED
        ).aggregate(total=Sum("total_amount"))["total"] or 0

        # Upcoming departures (next 30 days)
        upcoming_departures = Departure.objects.filter(
            departure_date__gte=now.date(),
            departure_date__lte=(now + timezone.timedelta(days=30)).date(),
            status=Departure.Status.AVAILABLE,
        ).select_related("package").order_by("departure_date")[:5]

        # Most booked packages
        top_packages = TourPackage.objects.annotate(
            total_reservations=Count("departures__reservations")
        ).order_by("-total_reservations")[:5]

        # Package occupancy
        package_occupancy = Departure.objects.filter(
            status__in=[Departure.Status.AVAILABLE, Departure.Status.FULL]
        ).select_related("package").annotate(
            occupancy=F("capacity") - F("available_slots")
        ).order_by("-occupancy")[:8]

        # Latest reservations
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
        # Reservations by status
        by_status = Reservation.objects.values("status").annotate(total=Count("id"))

        # Revenue by package
        revenue_by_package = Reservation.objects.filter(
            status=Reservation.Status.CONFIRMED
        ).values(
            pkg_name=F("departure__package__name")
        ).annotate(revenue=Sum("total_amount")).order_by("-revenue")[:10]

        # Reservations per month (last 6 months)
        # MySQL sin tablas de zona horaria: usar Extract en lugar de TruncMonth
        from django.db.models.functions import ExtractYear, ExtractMonth
        monthly = (
            Reservation.objects.annotate(
                year=ExtractYear("created_at"),
                month_num=ExtractMonth("created_at"),
            )
            .values("year", "month_num")
            .annotate(total=Count("id"))
            .order_by("-year", "-month_num")[:6]
        )

        context = {
            "by_status": list(by_status),
            "revenue_by_package": list(revenue_by_package),
            "monthly": list(monthly),
        }
        return render(request, self.template_name, context)

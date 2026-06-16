from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count, Sum, F
from apps.reservations.models import Reservation
from apps.packages.models import TourPackage
from apps.accounts.models import User


class ReportViewSet(ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        if not request.user.is_admin_role():
            return Response({"detail": "Sin permiso."}, status=403)

        data = {
            "total_users": User.objects.count(),
            "active_clients": User.objects.filter(role="CLIENT", status="ACTIVE").count(),
            "total_packages": TourPackage.objects.count(),
            "pending_reservations": Reservation.objects.filter(status="PENDING").count(),
            "confirmed_reservations": Reservation.objects.filter(status="CONFIRMED").count(),
            "total_revenue": Reservation.objects.filter(status="CONFIRMED").aggregate(
                t=Sum("total_amount")
            )["t"] or 0,
            "top_packages": list(
                TourPackage.objects.annotate(
                    total=Count("departures__reservations")
                ).values("name", "total").order_by("-total")[:5]
            ),
        }
        return Response(data)

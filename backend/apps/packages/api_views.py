from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import TourPackage, PackageDestination, Departure
from .serializers import TourPackageSerializer, PackageDestinationSerializer, DepartureSerializer


class TourPackageViewSet(viewsets.ModelViewSet):
    queryset = TourPackage.objects.prefetch_related("package_destinations__destination").all()
    serializer_class = TourPackageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "is_active"]
    search_fields = ["name", "public_code"]
    ordering_fields = ["price", "days", "created_at"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class PackageDestinationViewSet(viewsets.ModelViewSet):
    queryset = PackageDestination.objects.select_related("package", "destination").all()
    serializer_class = PackageDestinationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["package"]


class DepartureViewSet(viewsets.ModelViewSet):
    queryset = Departure.objects.select_related("package").all()
    serializer_class = DepartureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["package", "status"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Destination
from .serializers import DestinationSerializer


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.select_related("city__country").all()
    serializer_class = DestinationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["city", "city__country", "difficulty", "is_active"]
    search_fields = ["name", "public_code"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

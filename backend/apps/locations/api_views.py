from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Country, City
from .serializers import CountrySerializer, CitySerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "code"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related("country").all()
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["country"]
    search_fields = ["name"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

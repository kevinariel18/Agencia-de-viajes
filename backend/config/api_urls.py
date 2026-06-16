from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.accounts.api_views import UserViewSet
from apps.locations.api_views import CountryViewSet, CityViewSet
from apps.destinations.api_views import DestinationViewSet
from apps.packages.api_views import TourPackageViewSet, PackageDestinationViewSet, DepartureViewSet
from apps.reservations.api_views import ReservationViewSet
from apps.reports.api_views import ReportViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="api-users")
router.register(r"countries", CountryViewSet, basename="api-countries")
router.register(r"cities", CityViewSet, basename="api-cities")
router.register(r"destinations", DestinationViewSet, basename="api-destinations")
router.register(r"packages", TourPackageViewSet, basename="api-packages")
router.register(r"package-destinations", PackageDestinationViewSet, basename="api-pkg-dest")
router.register(r"departures", DepartureViewSet, basename="api-departures")
router.register(r"reservations", ReservationViewSet, basename="api-reservations")
router.register(r"reports", ReportViewSet, basename="api-reports")

urlpatterns = [
    path("auth/", include("apps.accounts.api_auth")),
    path("", include(router.urls)),
]

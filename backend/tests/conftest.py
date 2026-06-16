import pytest
import datetime
from decimal import Decimal
from django.utils import timezone


@pytest.fixture
def country(db):
    from apps.locations.models import Country
    return Country.objects.create(code="TS", name="TestCountry")


@pytest.fixture
def city(db, country):
    from apps.locations.models import City
    return City.objects.create(country=country, name="TestCity")


@pytest.fixture
def admin_user(db, city):
    from apps.accounts.models import User
    u = User(
        username="admin@test.com", email="admin@test.com",
        first_name="Admin", last_name="Test",
        role=User.Role.ADMIN, status=User.Status.ACTIVE,
        city=city, is_staff=True,
    )
    u.set_password("Admin123*")
    u.save()
    return u


@pytest.fixture
def client_user(db, city):
    from apps.accounts.models import User
    u = User(
        username="client@test.com", email="client@test.com",
        first_name="Cliente", last_name="Test",
        role=User.Role.CLIENT, status=User.Status.ACTIVE,
        city=city,
    )
    u.set_password("Cliente123*")
    u.save()
    return u


@pytest.fixture
def destination(db, city):
    from apps.destinations.models import Destination
    return Destination.objects.create(
        city=city, name="Destino Test",
        description="Descripción de prueba",
        difficulty="EASY",
    )


@pytest.fixture
def package(db):
    from apps.packages.models import TourPackage
    return TourPackage.objects.create(
        name="Paquete Test", description="Desc",
        days=5, nights=4, price=Decimal("500.00"),
        category="STANDARD",
    )


@pytest.fixture
def departure(db, package):
    from apps.packages.models import Departure
    return Departure.objects.create(
        package=package,
        departure_date=timezone.now().date() + datetime.timedelta(days=30),
        capacity=10,
        status="AVAILABLE",
    )


@pytest.fixture
def full_departure(db, package):
    from apps.packages.models import Departure
    dep = Departure.objects.create(
        package=package,
        departure_date=timezone.now().date() + datetime.timedelta(days=45),
        capacity=2,
        status="AVAILABLE",
    )
    dep.available_slots = 0
    dep.status = "FULL"
    dep.save()
    return dep

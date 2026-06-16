import pytest
import datetime
from decimal import Decimal
from django.utils import timezone
from apps.packages.models import TourPackage, Departure


@pytest.mark.django_db
class TestTourPackage:
    def test_create_package(self):
        pkg = TourPackage.objects.create(
            name="Paquete Nuevo", description="Desc",
            days=3, nights=2, price=Decimal("300.00"),
            category="STANDARD",
        )
        assert pkg.pk is not None
        assert pkg.public_code.startswith("PKG-")

    def test_price_required_positive(self):
        from django.core.exceptions import ValidationError
        pkg = TourPackage(
            name="Malo", description="x",
            days=1, nights=0, price=Decimal("0.00"),
            category="STANDARD",
        )
        with pytest.raises(Exception):
            pkg.full_clean()

    def test_package_category_choices(self, package):
        assert package.category in [c[0] for c in TourPackage.Category.choices]


@pytest.mark.django_db
class TestDeparture:
    def test_create_departure(self, package):
        dep = Departure.objects.create(
            package=package,
            departure_date=timezone.now().date() + datetime.timedelta(days=15),
            capacity=20,
        )
        assert dep.available_slots == 20
        assert dep.status == "AVAILABLE"

    def test_duplicate_departure_rejected(self, departure):
        with pytest.raises(Exception):
            Departure.objects.create(
                package=departure.package,
                departure_date=departure.departure_date,
                capacity=5,
            )

    def test_past_date_rejected(self, package):
        from django.core.exceptions import ValidationError
        dep = Departure(
            package=package,
            departure_date=datetime.date(2020, 1, 1),
            capacity=10,
        )
        with pytest.raises(ValidationError):
            dep.full_clean()

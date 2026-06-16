import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from apps.reservations.models import Reservation
from apps.reservations.services import create_reservation, confirm_reservation, cancel_reservation


@pytest.mark.django_db
class TestReservationCreate:
    def test_create_with_available_slots(self, client_user, departure):
        initial_slots = departure.available_slots
        res = create_reservation(client_user, departure.pk, 2)
        assert res.pk is not None
        assert res.public_code.startswith("RES-")
        departure.refresh_from_db()
        assert departure.available_slots == initial_slots - 2

    def test_total_calculated_correctly(self, client_user, departure):
        res = create_reservation(client_user, departure.pk, 3)
        assert res.total_amount == departure.package.price * 3

    def test_unit_price_from_package(self, client_user, departure):
        res = create_reservation(client_user, departure.pk, 1)
        assert res.unit_price == departure.package.price

    def test_create_fails_insufficient_slots(self, client_user, full_departure):
        with pytest.raises(ValidationError):
            create_reservation(client_user, full_departure.pk, 1)

    def test_slots_reach_zero_sets_full(self, client_user, departure):
        departure.available_slots = 2
        departure.capacity = 2
        departure.save()
        create_reservation(client_user, departure.pk, 2)
        departure.refresh_from_db()
        assert departure.status == "FULL"

    def test_cannot_reserve_more_than_available(self, client_user, departure):
        departure.available_slots = 3
        departure.save()
        with pytest.raises(ValidationError):
            create_reservation(client_user, departure.pk, 5)


@pytest.mark.django_db
class TestReservationConfirm:
    def test_confirm_pending_reservation(self, client_user, departure):
        res = create_reservation(client_user, departure.pk, 1)
        confirmed = confirm_reservation(res.pk)
        assert confirmed.status == "CONFIRMED"
        assert confirmed.payment_status == "PAID"

    def test_confirm_already_confirmed_is_idempotent(self, client_user, departure):
        res = create_reservation(client_user, departure.pk, 1)
        confirm_reservation(res.pk)
        result = confirm_reservation(res.pk)
        assert result.status == "CONFIRMED"

    def test_confirm_cancelled_raises(self, client_user, departure):
        res = create_reservation(client_user, departure.pk, 1)
        cancel_reservation(res.pk)
        with pytest.raises(ValidationError):
            confirm_reservation(res.pk)


@pytest.mark.django_db
class TestReservationCancel:
    def test_cancel_returns_slots(self, client_user, departure):
        slots_before = departure.available_slots
        res = create_reservation(client_user, departure.pk, 2)
        departure.refresh_from_db()
        assert departure.available_slots == slots_before - 2
        cancel_reservation(res.pk)
        departure.refresh_from_db()
        assert departure.available_slots == slots_before

    def test_cancel_sets_available_when_was_full(self, client_user, departure):
        departure.available_slots = 1
        departure.capacity = 1
        departure.save()
        res = create_reservation(client_user, departure.pk, 1)
        departure.refresh_from_db()
        assert departure.status == "FULL"
        cancel_reservation(res.pk)
        departure.refresh_from_db()
        assert departure.status == "AVAILABLE"

    def test_cancel_twice_raises(self, client_user, departure):
        res = create_reservation(client_user, departure.pk, 1)
        cancel_reservation(res.pk)
        with pytest.raises(ValidationError):
            cancel_reservation(res.pk)

    def test_paid_reservation_becomes_refunded(self, client_user, departure):
        res = create_reservation(client_user, departure.pk, 1)
        confirm_reservation(res.pk)
        cancelled = cancel_reservation(res.pk)
        assert cancelled.payment_status == "REFUNDED"


@pytest.mark.django_db
class TestReservationAccess:
    def test_client_only_sees_own_reservations(self, client_user, departure, admin_user):
        from apps.accounts.models import User
        other = User(
            username="other@x.com", email="other@x.com",
            first_name="Other", last_name="User",
            role=User.Role.CLIENT, status=User.Status.ACTIVE,
        )
        other.set_password("pass")
        other.save()
        my_res = create_reservation(client_user, departure.pk, 1)
        from apps.packages.models import Departure
        import datetime
        from django.utils import timezone
        dep2 = Departure.objects.create(
            package=departure.package,
            departure_date=timezone.now().date() + datetime.timedelta(days=120),
            capacity=10,
        )
        other_res = create_reservation(other, dep2.pk, 1)
        my_qs = Reservation.objects.filter(user=client_user)
        assert my_res in my_qs
        assert other_res not in my_qs

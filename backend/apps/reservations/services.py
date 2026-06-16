"""
Reservation business logic.
All slot management happens here using transaction.atomic + select_for_update
to prevent race conditions when multiple users book simultaneously.
"""
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Reservation
from apps.packages.models import Departure


def create_reservation(user, departure_id: int, number_of_people: int) -> Reservation:
    """
    Creates a new reservation and deducts slots atomically.
    Raises ValidationError if not enough slots are available.
    """
    with transaction.atomic():
        # Lock the departure row to prevent concurrent bookings
        departure = Departure.objects.select_for_update().get(pk=departure_id)

        if departure.status != Departure.Status.AVAILABLE:
            raise ValidationError("Esta fecha de salida no está disponible.")

        if departure.available_slots < number_of_people:
            raise ValidationError(
                f"No hay cupos suficientes. Disponibles: {departure.available_slots}."
            )

        unit_price = departure.package.price

        reservation = Reservation.objects.create(
            user=user,
            departure=departure,
            number_of_people=number_of_people,
            unit_price=unit_price,
            status=Reservation.Status.PENDING,
            payment_status=Reservation.PaymentStatus.PENDING,
        )

        # Deduct slots
        departure.available_slots -= number_of_people
        if departure.available_slots == 0:
            departure.status = Departure.Status.FULL
        departure.save()

    return reservation


def confirm_reservation(reservation_id: int) -> Reservation:
    """
    Confirms a PENDING reservation.
    Re-validates slots in case state changed since creation.
    """
    with transaction.atomic():
        reservation = Reservation.objects.select_for_update().get(pk=reservation_id)

        if reservation.status == Reservation.Status.CONFIRMED:
            return reservation  # already confirmed, idempotent

        if reservation.status == Reservation.Status.CANCELLED:
            raise ValidationError("No se puede confirmar una reserva cancelada.")

        reservation.status = Reservation.Status.CONFIRMED
        reservation.payment_status = Reservation.PaymentStatus.PAID
        reservation.save()

    return reservation


def cancel_reservation(reservation_id: int, cancelled_by_admin: bool = False) -> Reservation:
    """
    Cancels a reservation and returns the slots to the departure.
    """
    with transaction.atomic():
        reservation = Reservation.objects.select_for_update().get(pk=reservation_id)

        if reservation.status == Reservation.Status.CANCELLED:
            raise ValidationError("La reserva ya está cancelada.")

        departure = Departure.objects.select_for_update().get(pk=reservation.departure_id)

        # Only return slots if the reservation had consumed them (not if it was just PENDING)
        slots_to_return = reservation.number_of_people
        departure.available_slots = min(
            departure.available_slots + slots_to_return,
            departure.capacity
        )
        if departure.available_slots > 0 and departure.status == Departure.Status.FULL:
            departure.status = Departure.Status.AVAILABLE
        departure.save()

        reservation.status = Reservation.Status.CANCELLED
        if reservation.payment_status == Reservation.PaymentStatus.PAID:
            reservation.payment_status = Reservation.PaymentStatus.REFUNDED
        reservation.save()

    return reservation

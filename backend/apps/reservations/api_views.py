from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from .models import Reservation
from .serializers import ReservationSerializer, ReservationCreateSerializer
from .services import create_reservation, confirm_reservation, cancel_reservation


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_role():
            return Reservation.objects.select_related("user", "departure__package").all()
        return Reservation.objects.filter(user=user).select_related("departure__package")

    def create(self, request, *args, **kwargs):
        serializer = ReservationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            reservation = create_reservation(
                user=request.user,
                departure_id=serializer.validated_data["departure_id"],
                number_of_people=serializer.validated_data["number_of_people"],
            )
            return Response(ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        if not request.user.is_admin_role():
            return Response({"detail": "Sin permiso."}, status=403)
        try:
            reservation = confirm_reservation(pk)
            return Response(ReservationSerializer(reservation).data)
        except ValidationError as e:
            return Response({"detail": e.message}, status=400)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        if not request.user.is_admin_role() and reservation.user != request.user:
            return Response({"detail": "Sin permiso."}, status=403)
        try:
            reservation = cancel_reservation(pk, cancelled_by_admin=request.user.is_admin_role())
            return Response(ReservationSerializer(reservation).data)
        except ValidationError as e:
            return Response({"detail": e.message}, status=400)

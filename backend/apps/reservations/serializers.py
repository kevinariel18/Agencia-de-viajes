from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)
    package_name = serializers.CharField(source="departure.package.name", read_only=True)
    departure_date = serializers.DateField(source="departure.departure_date", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Reservation
        fields = (
            "id", "public_code", "user", "user_name", "departure",
            "package_name", "departure_date", "reservation_date",
            "number_of_people", "unit_price", "total_amount",
            "payment_status", "status", "status_display",
        )
        read_only_fields = ("public_code", "reservation_date", "total_amount", "unit_price")


class ReservationCreateSerializer(serializers.Serializer):
    departure_id = serializers.IntegerField()
    number_of_people = serializers.IntegerField(min_value=1)

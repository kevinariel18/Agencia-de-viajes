from rest_framework import serializers
from .models import Destination


class DestinationSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source="city.name", read_only=True)
    country_name = serializers.CharField(source="city.country.name", read_only=True)
    difficulty_display = serializers.CharField(source="get_difficulty_display", read_only=True)

    class Meta:
        model = Destination
        fields = (
            "id", "public_code", "city", "city_name", "country_name",
            "name", "description", "attractions", "climate", "season",
            "difficulty", "difficulty_display", "image", "is_active",
        )
        read_only_fields = ("public_code",)

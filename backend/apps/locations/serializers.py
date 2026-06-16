from rest_framework import serializers
from .models import Country, City


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "code", "name", "is_active", "created_at")
        read_only_fields = ("created_at",)


class CitySerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source="country.name", read_only=True)

    class Meta:
        model = City
        fields = ("id", "country", "country_name", "name", "phone_prefix", "postal_code", "region_zone", "is_active")

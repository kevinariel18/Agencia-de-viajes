from rest_framework import serializers
from .models import TourPackage, PackageDestination, Departure


class PackageDestinationSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(source="destination.name", read_only=True)

    class Meta:
        model = PackageDestination
        fields = ("id", "package", "destination", "destination_name", "visit_order")


class DepartureSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(source="package.name", read_only=True)

    class Meta:
        model = Departure
        fields = ("id", "package", "package_name", "departure_date", "capacity", "available_slots", "status")
        read_only_fields = ("available_slots",)


class TourPackageSerializer(serializers.ModelSerializer):
    package_destinations = PackageDestinationSerializer(many=True, read_only=True)
    next_departure = serializers.SerializerMethodField()
    category_display = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = TourPackage
        fields = (
            "id", "public_code", "name", "description", "days", "nights",
            "price", "category", "category_display", "includes", "stops",
            "image", "is_active", "package_destinations", "next_departure",
        )
        read_only_fields = ("public_code",)

    def get_next_departure(self, obj):
        dep = obj.get_next_departure()
        if dep:
            return DepartureSerializer(dep).data
        return None

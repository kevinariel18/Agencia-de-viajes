from django.contrib import admin
from .models import TourPackage, PackageDestination, Departure


class PackageDestinationInline(admin.TabularInline):
    model = PackageDestination
    extra = 1


class DepartureInline(admin.TabularInline):
    model = Departure
    extra = 1
    readonly_fields = ("available_slots",)


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ("public_code", "name", "category", "price", "days", "is_active")
    list_filter = ("is_active", "category")
    search_fields = ("name", "public_code")
    ordering = ("-created_at",)
    readonly_fields = ("public_code", "created_at", "updated_at")
    inlines = [PackageDestinationInline, DepartureInline]


@admin.register(PackageDestination)
class PackageDestinationAdmin(admin.ModelAdmin):
    list_display = ("package", "destination", "visit_order")
    list_filter = ("package",)
    ordering = ("package", "visit_order")


@admin.register(Departure)
class DepartureAdmin(admin.ModelAdmin):
    list_display = ("package", "departure_date", "capacity", "available_slots", "status")
    list_filter = ("status", "package")
    search_fields = ("package__name",)
    ordering = ("departure_date",)
    readonly_fields = ("created_at", "updated_at")

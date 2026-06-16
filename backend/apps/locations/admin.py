from django.contrib import admin
from .models import Country, City


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("code", "name")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "phone_prefix", "is_active")
    list_filter = ("is_active", "country")
    search_fields = ("name", "country__name")
    ordering = ("country__name", "name")
    readonly_fields = ("created_at", "updated_at")

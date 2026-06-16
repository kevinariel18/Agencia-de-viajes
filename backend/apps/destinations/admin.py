from django.contrib import admin
from .models import Destination


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("public_code", "name", "city", "difficulty", "is_active")
    list_filter = ("is_active", "difficulty", "city__country")
    search_fields = ("name", "public_code", "city__name")
    ordering = ("name",)
    readonly_fields = ("public_code", "created_at", "updated_at")

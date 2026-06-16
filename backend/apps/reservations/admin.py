from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("public_code", "user", "departure", "number_of_people", "total_amount", "status", "payment_status")
    list_filter = ("status", "payment_status")
    search_fields = ("public_code", "user__email", "user__first_name")
    ordering = ("-created_at",)
    readonly_fields = ("public_code", "reservation_date", "total_amount", "created_at", "updated_at")

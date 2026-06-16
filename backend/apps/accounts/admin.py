from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("public_code", "email", "get_full_name", "role", "status", "created_at")
    list_filter = ("role", "status", "is_staff")
    search_fields = ("email", "first_name", "last_name", "public_code")
    ordering = ("-created_at",)
    readonly_fields = ("public_code", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Información personal", {"fields": ("first_name", "last_name", "phone", "city")}),
        ("Rol y estado", {"fields": ("role", "status", "public_code")}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Fechas", {"fields": ("last_login", "date_joined", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "first_name", "last_name", "role", "password1", "password2"),
        }),
    )

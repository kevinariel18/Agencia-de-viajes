import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("locations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                ("is_superuser", models.BooleanField(default=False)),
                ("username", models.CharField(
                    max_length=150, unique=True,
                    validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                )),
                ("first_name", models.CharField(blank=True, max_length=150)),
                ("last_name", models.CharField(blank=True, max_length=150)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now)),
                ("public_code", models.CharField(
                    blank=True, max_length=20, unique=True,
                    validators=[django.core.validators.RegexValidator(r"^USR-\d+$", "Formato: USR-001")],
                )),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("city", models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name="users",
                    to="locations.city",
                )),
                ("role", models.CharField(
                    choices=[("ADMIN", "Administrador"), ("CLIENT", "Cliente")],
                    default="CLIENT", max_length=10,
                )),
                ("status", models.CharField(
                    choices=[("ACTIVE", "Activo"), ("INACTIVE", "Inactivo"), ("SUSPENDED", "Suspendido")],
                    default="ACTIVE", max_length=15,
                )),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("groups", models.ManyToManyField(
                    blank=True, related_name="user_set", related_query_name="user",
                    to="auth.group", verbose_name="groups",
                )),
                ("user_permissions", models.ManyToManyField(
                    blank=True, related_name="user_set", related_query_name="user",
                    to="auth.permission", verbose_name="user permissions",
                )),
            ],
            options={
                "verbose_name": "Usuario",
                "verbose_name_plural": "Usuarios",
                "ordering": ["-created_at"],
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]

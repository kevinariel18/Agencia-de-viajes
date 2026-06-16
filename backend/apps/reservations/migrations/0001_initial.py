import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("packages", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Reservation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("public_code", models.CharField(
                    blank=True, max_length=20, unique=True,
                    validators=[django.core.validators.RegexValidator(r"^RES-\d+$", "Formato: RES-1001")],
                )),
                ("user", models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="reservations",
                    to=settings.AUTH_USER_MODEL,
                )),
                ("departure", models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="reservations",
                    to="packages.departure",
                )),
                ("reservation_date", models.DateTimeField(auto_now_add=True)),
                ("number_of_people", models.PositiveIntegerField(
                    validators=[django.core.validators.MinValueValidator(1)]
                )),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("total_amount", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("payment_status", models.CharField(
                    choices=[
                        ("PENDING", "Pendiente"), ("PAID", "Pagado"),
                        ("REFUNDED", "Reembolsado"), ("FAILED", "Fallido"),
                    ],
                    default="PENDING", max_length=15,
                )),
                ("status", models.CharField(
                    choices=[
                        ("PENDING", "Pendiente"), ("CONFIRMED", "Confirmada"),
                        ("IN_PROCESS", "En proceso"), ("CANCELLED", "Cancelada"),
                    ],
                    default="PENDING", max_length=15,
                )),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Reserva",
                "verbose_name_plural": "Reservas",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="reservation",
            index=models.Index(fields=["status"], name="reservations_status_idx"),
        ),
        migrations.AddIndex(
            model_name="reservation",
            index=models.Index(fields=["user"], name="reservations_user_idx"),
        ),
    ]

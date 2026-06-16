import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("destinations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TourPackage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("public_code", models.CharField(
                    blank=True, max_length=20, unique=True,
                    validators=[django.core.validators.RegexValidator(r"^PKG-\d+$", "Formato: PKG-001")],
                )),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("days", models.PositiveIntegerField(
                    validators=[django.core.validators.MinValueValidator(1)]
                )),
                ("nights", models.PositiveIntegerField(default=0)),
                ("price", models.DecimalField(
                    decimal_places=2, max_digits=10,
                    validators=[django.core.validators.MinValueValidator(0.01)],
                )),
                ("category", models.CharField(
                    choices=[
                        ("STANDARD", "Estándar"), ("PREMIUM", "Premium"),
                        ("ADVENTURE", "Aventura"), ("LUXURY", "Lujo"), ("ECOLOGICAL", "Ecológico"),
                    ],
                    default="STANDARD", max_length=15,
                )),
                ("includes", models.TextField(blank=True)),
                ("stops", models.TextField(blank=True)),
                ("image", models.ImageField(blank=True, null=True, upload_to="packages/")),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Paquete Turístico",
                "verbose_name_plural": "Paquetes Turísticos",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="tourpackage",
            index=models.Index(fields=["category"], name="packages_tp_cat_idx"),
        ),
        migrations.AddIndex(
            model_name="tourpackage",
            index=models.Index(fields=["price"], name="packages_tp_price_idx"),
        ),
        migrations.CreateModel(
            name="PackageDestination",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("package", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="package_destinations",
                    to="packages.tourpackage",
                )),
                ("destination", models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="package_destinations",
                    to="destinations.destination",
                )),
                ("visit_order", models.PositiveIntegerField(default=1)),
            ],
            options={
                "verbose_name": "Destino del Paquete",
                "verbose_name_plural": "Destinos del Paquete",
                "ordering": ["visit_order"],
            },
        ),
        migrations.AddConstraint(
            model_name="packagedestination",
            constraint=models.UniqueConstraint(
                fields=["package", "destination"],
                name="unique_package_destination",
            ),
        ),
        migrations.CreateModel(
            name="Departure",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("package", models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="departures",
                    to="packages.tourpackage",
                )),
                ("departure_date", models.DateField()),
                ("capacity", models.PositiveIntegerField(
                    validators=[django.core.validators.MinValueValidator(1)]
                )),
                ("available_slots", models.PositiveIntegerField(default=0)),
                ("status", models.CharField(
                    choices=[
                        ("AVAILABLE", "Disponible"), ("FULL", "Lleno"),
                        ("CANCELLED", "Cancelado"), ("COMPLETED", "Completado"),
                    ],
                    default="AVAILABLE", max_length=15,
                )),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Fecha de Salida",
                "verbose_name_plural": "Fechas de Salida",
                "ordering": ["departure_date"],
            },
        ),
        migrations.AddConstraint(
            model_name="departure",
            constraint=models.UniqueConstraint(
                fields=["package", "departure_date"],
                name="unique_package_departure_date",
            ),
        ),
        migrations.AddIndex(
            model_name="departure",
            index=models.Index(
                fields=["departure_date", "status"],
                name="packages_dep_date_status_idx",
            ),
        ),
    ]

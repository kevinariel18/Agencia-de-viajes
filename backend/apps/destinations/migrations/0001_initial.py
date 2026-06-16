import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("locations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Destination",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("public_code", models.CharField(
                    blank=True, max_length=20, unique=True,
                    validators=[django.core.validators.RegexValidator(r"^DST-\d+$", "Formato: DST-001")],
                )),
                ("city", models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="destinations",
                    to="locations.city",
                )),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("attractions", models.TextField(blank=True)),
                ("climate", models.CharField(blank=True, max_length=100)),
                ("season", models.CharField(blank=True, max_length=100)),
                ("difficulty", models.CharField(
                    choices=[("EASY", "Fácil"), ("MODERATE", "Moderado"), ("HIGH", "Alto")],
                    default="EASY", max_length=10,
                )),
                ("image", models.ImageField(blank=True, null=True, upload_to="destinations/")),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Destino",
                "verbose_name_plural": "Destinos",
                "ordering": ["name"],
            },
        ),
        migrations.AddIndex(
            model_name="destination",
            index=models.Index(fields=["name"], name="destinations_name_idx"),
        ),
        migrations.AddIndex(
            model_name="destination",
            index=models.Index(fields=["difficulty"], name="destinations_diff_idx"),
        ),
    ]

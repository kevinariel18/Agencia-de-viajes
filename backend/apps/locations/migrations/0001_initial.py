from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("code", models.CharField(max_length=5, unique=True)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name": "País", "verbose_name_plural": "Países", "ordering": ["name"]},
        ),
        migrations.AddIndex(
            model_name="country",
            index=models.Index(fields=["code"], name="locations_c_code_idx"),
        ),
        migrations.AddIndex(
            model_name="country",
            index=models.Index(fields=["name"], name="locations_c_name_idx"),
        ),
        migrations.CreateModel(
            name="City",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("country", models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="cities",
                    to="locations.country",
                )),
                ("name", models.CharField(max_length=100)),
                ("phone_prefix", models.CharField(blank=True, max_length=10)),
                ("postal_code", models.CharField(blank=True, max_length=15)),
                ("region_zone", models.CharField(blank=True, max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Ciudad",
                "verbose_name_plural": "Ciudades",
                "ordering": ["country__name", "name"],
            },
        ),
        migrations.AddIndex(
            model_name="city",
            index=models.Index(fields=["name"], name="locations_ci_name_idx"),
        ),
    ]

from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=5, unique=True, verbose_name="Código")
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
        ordering = ["name"]
        indexes = [models.Index(fields=["code"]), models.Index(fields=["name"])]

    def __str__(self):
        return f"{self.name} ({self.code})"


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name="País", related_name="cities")
    name = models.CharField(max_length=100, verbose_name="Nombre")
    phone_prefix = models.CharField(max_length=10, blank=True, verbose_name="Prefijo telefónico")
    postal_code = models.CharField(max_length=15, blank=True, verbose_name="Código postal")
    region_zone = models.CharField(max_length=100, blank=True, verbose_name="Zona/Región")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"
        ordering = ["country__name", "name"]
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return f"{self.name}, {self.country.name}"

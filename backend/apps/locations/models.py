from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
        ordering = ["name"]
        indexes = [models.Index(fields=["code"]), models.Index(fields=["name"])]

    def __str__(self):
        return f"{self.name} ({self.code})"


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="cities")
    name = models.CharField(max_length=100)
    phone_prefix = models.CharField(max_length=10, blank=True)
    postal_code = models.CharField(max_length=15, blank=True)
    region_zone = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"
        ordering = ["country__name", "name"]
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return f"{self.name}, {self.country.name}"

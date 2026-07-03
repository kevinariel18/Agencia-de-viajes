from django.db import models
from django.core.validators import RegexValidator


class Destination(models.Model):
    class Difficulty(models.TextChoices):
        EASY = "EASY", "Fácil"
        MODERATE = "MODERATE", "Moderado"
        HIGH = "HIGH", "Alto"

    public_code = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        verbose_name="Código público",
        validators=[RegexValidator(r"^DST-\d+$", "Formato: DST-001")],
    )
    city = models.ForeignKey(
        "locations.City",
        on_delete=models.PROTECT,
        verbose_name="Ciudad",
        related_name="destinations",
    )
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    attractions = models.TextField(blank=True, verbose_name="Atractivos")
    climate = models.CharField(max_length=100, blank=True, verbose_name="Clima")
    season = models.CharField(max_length=100, blank=True, verbose_name="Temporada")
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices, default=Difficulty.EASY, verbose_name="Dificultad")
    image = models.ImageField(upload_to="destinations/", null=True, blank=True, verbose_name="Imagen")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Destino"
        verbose_name_plural = "Destinos"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["difficulty"]),
        ]

    def __str__(self):
        return f"{self.public_code} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.public_code:
            count = Destination.objects.count()
            self.public_code = f"DST-{count + 1:03d}"
        super().save(*args, **kwargs)

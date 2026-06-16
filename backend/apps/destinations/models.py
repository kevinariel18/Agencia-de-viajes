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
        validators=[RegexValidator(r"^DST-\d+$", "Formato: DST-001")],
    )
    city = models.ForeignKey(
        "locations.City",
        on_delete=models.PROTECT,
        related_name="destinations",
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    attractions = models.TextField(blank=True)
    climate = models.CharField(max_length=100, blank=True)
    season = models.CharField(max_length=100, blank=True)
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices, default=Difficulty.EASY)
    image = models.ImageField(upload_to="destinations/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

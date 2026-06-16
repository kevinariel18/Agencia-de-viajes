from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.utils import timezone


class TourPackage(models.Model):
    class Category(models.TextChoices):
        STANDARD = "STANDARD", "Estándar"
        PREMIUM = "PREMIUM", "Premium"
        ADVENTURE = "ADVENTURE", "Aventura"
        LUXURY = "LUXURY", "Lujo"
        ECOLOGICAL = "ECOLOGICAL", "Ecológico"

    public_code = models.CharField(
        max_length=20, unique=True, blank=True,
        validators=[RegexValidator(r"^PKG-\d+$", "Formato: PKG-001")],
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    days = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    nights = models.PositiveIntegerField(default=0)
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    category = models.CharField(max_length=15, choices=Category.choices, default=Category.STANDARD)
    # Relaciones opcionales que reflejan el diagrama físico
    category_obj = models.ForeignKey(
        "packages.PackageCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="packages",
    )
    provider = models.ForeignKey(
        "packages.Provider",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="packages",
    )
    transport = models.ForeignKey(
        "packages.Transport",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="packages",
    )
    capacity = models.PositiveIntegerField(null=True, blank=True)
    includes = models.TextField(blank=True)
    stops = models.TextField(blank=True)
    image = models.ImageField(upload_to="packages/", null=True, blank=True)
    image_url = models.URLField(
        max_length=500, null=True, blank=True,
        verbose_name="URL de imagen",
        help_text="URL de imagen de internet (Unsplash, Pexels). Se usa si no hay imagen subida.",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paquete Turístico"
        verbose_name_plural = "Paquetes Turísticos"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["price"]),
        ]

    def __str__(self):
        return f"{self.public_code} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.public_code:
            count = TourPackage.objects.count()
            self.public_code = f"PKG-{count + 1:03d}"
        super().save(*args, **kwargs)

    def get_next_departure(self):
        return self.departures.filter(
            status="AVAILABLE",
            departure_date__gte=timezone.now().date(),
        ).order_by("departure_date").first()

    def get_image_src(self):
        """Imagen subida tiene prioridad sobre URL."""
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return None


class PackageCategory(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Categoría de Paquete"
        verbose_name_plural = "Categorías de Paquetes"

    def __str__(self):
        return self.name


class Provider(models.Model):
    ruc = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=200, blank=True)
    country = models.ForeignKey(
        "locations.Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="providers",
    )

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.name


class Transport(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=250, blank=True)

    class Meta:
        verbose_name = "Transporte"
        verbose_name_plural = "Transportes"

    def __str__(self):
        return self.name


class Scale(models.Model):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    city = models.ForeignKey(
        "locations.City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="scales",
    )

    class Meta:
        verbose_name = "Escala"
        verbose_name_plural = "Escalas"

    def __str__(self):
        return self.name


class PackageScale(models.Model):
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name="package_scales")
    scale = models.ForeignKey(Scale, on_delete=models.CASCADE, related_name="package_scales")
    visit_order = models.PositiveIntegerField(default=1)
    departure_time = models.TimeField(null=True, blank=True)
    arrival_time = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Escala del Paquete"
        verbose_name_plural = "Escalas del Paquete"
        ordering = ["visit_order"]
        constraints = [
            models.UniqueConstraint(fields=["package", "scale"], name="unique_package_scale")
        ]

    def __str__(self):
        return f"{self.package.name} - {self.scale.name} (orden {self.visit_order})"


class PackageDestination(models.Model):
    package = models.ForeignKey(
        TourPackage, on_delete=models.CASCADE, related_name="package_destinations"
    )
    destination = models.ForeignKey(
        "destinations.Destination",
        on_delete=models.PROTECT,
        related_name="package_destinations",
    )
    visit_order = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Destino del Paquete"
        verbose_name_plural = "Destinos del Paquete"
        ordering = ["visit_order"]
        constraints = [
            models.UniqueConstraint(
                fields=["package", "destination"],
                name="unique_package_destination",
            )
        ]

    def __str__(self):
        return f"{self.package.name} → {self.destination.name} (orden {self.visit_order})"


class Departure(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Disponible"
        FULL = "FULL", "Lleno"
        CANCELLED = "CANCELLED", "Cancelado"
        COMPLETED = "COMPLETED", "Completado"

    package = models.ForeignKey(TourPackage, on_delete=models.PROTECT, related_name="departures")
    departure_date = models.DateField()
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    available_slots = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fecha de Salida"
        verbose_name_plural = "Fechas de Salida"
        ordering = ["departure_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["package", "departure_date"],
                name="unique_package_departure_date",
            )
        ]
        indexes = [models.Index(fields=["departure_date", "status"])]

    def __str__(self):
        return f"{self.package.name} — {self.departure_date}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.departure_date and self.departure_date < timezone.now().date():
            raise ValidationError({"departure_date": "La fecha no puede ser anterior a hoy."})
        if self.capacity and self.available_slots > self.capacity:
            raise ValidationError({"available_slots": "No puede superar la capacidad."})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.available_slots = self.capacity
        super().save(*args, **kwargs)

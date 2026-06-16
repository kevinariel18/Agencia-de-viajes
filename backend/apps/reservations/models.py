from django.db import models
from django.core.validators import RegexValidator, MinValueValidator


class Reservation(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        CONFIRMED = "CONFIRMED", "Confirmada"
        IN_PROCESS = "IN_PROCESS", "En proceso"
        CANCELLED = "CANCELLED", "Cancelada"

    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        PAID = "PAID", "Pagado"
        REFUNDED = "REFUNDED", "Reembolsado"
        FAILED = "FAILED", "Fallido"

    public_code = models.CharField(
        max_length=20, unique=True, blank=True,
        validators=[RegexValidator(r"^RES-\d+$", "Formato: RES-1001")],
    )
    user = models.ForeignKey(
        "accounts.User", on_delete=models.PROTECT, related_name="reservations"
    )
    departure = models.ForeignKey(
        "packages.Departure", on_delete=models.PROTECT, related_name="reservations"
    )
    reservation_date = models.DateTimeField(auto_now_add=True)
    number_of_people = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_status = models.CharField(
        max_length=15, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.public_code} — {self.user.get_full_name()}"

    def save(self, *args, **kwargs):
        if not self.public_code:
            count = Reservation.objects.count()
            self.public_code = f"RES-{1001 + count}"
        # Recalculate total
        if self.unit_price and self.number_of_people:
            self.total_amount = self.unit_price * self.number_of_people
        super().save(*args, **kwargs)


class Invoice(models.Model):
    number = models.AutoField(primary_key=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    issued_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.ForeignKey(
        "packages.PackageCategory", on_delete=models.SET_NULL, null=True, blank=True
    )
    customer = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="invoices"
    )

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"

    def __str__(self):
        return f"Factura #{self.number} - {self.issued_at.date()}"


class InvoicePackage(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="invoice_packages")
    package = models.ForeignKey("packages.TourPackage", on_delete=models.PROTECT, related_name="invoice_packages")
    package_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    days = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = "Factura - Paquete"
        verbose_name_plural = "Facturas - Paquetes"
        unique_together = ("invoice", "package")

    def __str__(self):
        return f"Factura #{self.invoice.number} — {self.package.name}"

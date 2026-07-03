from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        CLIENT = "CLIENT", "Cliente"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Activo"
        INACTIVE = "INACTIVE", "Inactivo"
        SUSPENDED = "SUSPENDED", "Suspendido"

    public_code = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        verbose_name="Código público",
        validators=[RegexValidator(r"^USR-\d+$", "Formato: USR-001")],
    )
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    city = models.ForeignKey(
        "locations.City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Ciudad",
        related_name="users",
    )
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT, verbose_name="Rol")
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.ACTIVE, verbose_name="Estado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    # Login con email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    def is_client_role(self):
        return self.role == self.Role.CLIENT

    def save(self, *args, **kwargs):
        # Assign public_code before first save
        if not self.public_code:
            # Use pk if available (update), otherwise count + 1
            count = User.objects.count()
            self.public_code = f"USR-{count + 1:03d}"
        super().save(*args, **kwargs)


class SalesAgent(models.Model):
    cedula = models.CharField(max_length=30, primary_key=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80, blank=True)
    position = models.CharField(max_length=80, blank=True)
    commission_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Agente de Venta"
        verbose_name_plural = "Agentes de Venta"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.cedula})"

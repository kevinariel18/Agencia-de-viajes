from django import forms
from django.utils import timezone
from .models import TourPackage, PackageDestination, Departure


class TourPackageForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = ("name", "description", "days", "nights", "price", "category", "includes", "stops", "image", "image_url", "is_active")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "days": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "nights": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0.01"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "includes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "stops": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "image_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://ejemplo.com/imagen.jpg"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "name": "Nombre", "description": "Descripción",
            "days": "Días", "nights": "Noches", "price": "Precio ($)",
            "category": "Categoría", "includes": "Incluye", "stops": "Paradas",
            "image": "Imagen", "image_url": "URL de imagen", "is_active": "Activo",
        }


class PackageDestinationForm(forms.ModelForm):
    class Meta:
        model = PackageDestination
        fields = ("destination", "visit_order")
        widgets = {
            "destination": forms.Select(attrs={"class": "form-select"}),
            "visit_order": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }
        labels = {"destination": "Destino", "visit_order": "Orden de visita"}


class DepartureForm(forms.ModelForm):
    class Meta:
        model = Departure
        fields = ("package", "departure_date", "capacity", "status")
        widgets = {
            "package": forms.Select(attrs={"class": "form-select"}),
            "departure_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "capacity": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "package": "Paquete", "departure_date": "Fecha de salida",
            "capacity": "Capacidad", "status": "Estado",
        }

    def clean_departure_date(self):
        date = self.cleaned_data.get("departure_date")
        if date and date < timezone.now().date():
            raise forms.ValidationError("La fecha debe ser posterior a hoy.")
        return date


class PackageFilterForm(forms.Form):
    q = forms.CharField(required=False, label="Buscar", widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Buscar..."}))
    category = forms.ChoiceField(
        required=False, label="Categoría",
        choices=[("", "Todas las categorías")] + TourPackage.Category.choices,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    price_min = forms.DecimalField(required=False, label="Precio mínimo", widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Precio mín."}))
    price_max = forms.DecimalField(required=False, label="Precio máximo", widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Precio máx."}))
    days = forms.IntegerField(required=False, label="Duración", widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Duración"}))

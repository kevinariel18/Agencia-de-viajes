from django import forms
from .models import Country, City


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ("code", "name", "is_active")
        widgets = {
            "code": forms.TextInput(attrs={"class": "form-control", "placeholder": "EC"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ecuador"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {"code": "Código", "name": "Nombre", "is_active": "Activo"}


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ("country", "name", "phone_prefix", "postal_code", "region_zone", "is_active")
        widgets = {
            "country": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_prefix": forms.TextInput(attrs={"class": "form-control", "placeholder": "+593"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control"}),
            "region_zone": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "country": "País", "name": "Nombre", "phone_prefix": "Prefijo telefónico",
            "postal_code": "Código postal", "region_zone": "Zona/Región", "is_active": "Activo",
        }

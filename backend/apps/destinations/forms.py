from django import forms
from .models import Destination


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ("city", "name", "description", "attractions", "climate", "season", "difficulty", "image", "is_active")
        widgets = {
            "city": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "attractions": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "climate": forms.TextInput(attrs={"class": "form-control"}),
            "season": forms.TextInput(attrs={"class": "form-control"}),
            "difficulty": forms.Select(attrs={"class": "form-select"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "city": "Ciudad", "name": "Nombre", "description": "Descripción",
            "attractions": "Atractivos", "climate": "Clima", "season": "Temporada",
            "difficulty": "Dificultad", "image": "Imagen", "is_active": "Activo",
        }

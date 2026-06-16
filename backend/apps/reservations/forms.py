from django import forms
from .models import Reservation


class ReservationCreateForm(forms.Form):
    departure_id = forms.IntegerField(widget=forms.HiddenInput)
    number_of_people = forms.IntegerField(
        label="Número de personas",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1}),
    )


class ReservationFilterForm(forms.Form):
    status = forms.ChoiceField(
        required=False,
        choices=[("", "Todos los estados")] + Reservation.Status.choices,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Buscar por código o usuario"}),
    )

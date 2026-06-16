from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from .models import User


class LoginForm(AuthenticationForm):
    """Login usando email como campo de usuario."""
    username = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "correo@ejemplo.com",
            "autofocus": True,
        }),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "••••••••",
        }),
    )


class ClientRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nombres",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label="Apellidos",
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    phone = forms.CharField(
        label="Teléfono",
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo electrónico.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.phone = self.cleaned_data.get("phone", "")
        user.role = User.Role.CLIENT
        user.status = User.Status.ACTIVE
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone", "city")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "phone": "Teléfono",
            "city": "Ciudad",
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

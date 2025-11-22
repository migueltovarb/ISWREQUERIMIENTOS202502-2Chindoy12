from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Mascota, Cita


class RegistroForm(forms.ModelForm):
    """Formulario de registro de usuario con validación de contraseña."""

    username = forms.CharField(
        label="Nombre",
        max_length=30,
        widget=forms.TextInput(attrs={"placeholder": "Tu nombre"})
    )

    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"placeholder": "Correo"})
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña"}),
        min_length=6,
    )

    confirmar_password = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmar contraseña"}),
        min_length=6,
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password")
        p2 = cleaned.get("confirmar_password")
        if p1 or p2:
            if not p1:
                raise ValidationError({'password': "La contraseña es obligatoria"})
            if not p2:
                raise ValidationError({'confirmar_password': "Confirma la contraseña"})
            if p1 != p2:
                raise ValidationError("Las contraseñas no coinciden")
        return cleaned


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'fecha_nacimiento', 'sexo', 'peso_kg']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['mascota', 'veterinario', 'fecha_inicio', 'fecha_fin', 'tipo', 'motivo']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned = super().clean()
        inicio = cleaned.get('fecha_inicio')
        fin = cleaned.get('fecha_fin')
        if inicio and fin and fin <= inicio:
            raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio')
        return cleaned

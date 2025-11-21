from django import forms
from django.contrib.auth.models import User
from .models import Mascota, Cita

class RegistroForm(forms.ModelForm):
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
        widget=forms.PasswordInput(attrs={"placeholder": "Contraseña"})
    )

    confirmar_password = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmar contraseña"})
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean(self):
        datos = super().clean()
        p1 = datos.get("password")
        p2 = datos.get("confirmar_password")

        if p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return datos


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

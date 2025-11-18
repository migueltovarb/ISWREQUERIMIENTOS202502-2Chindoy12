from django import forms
from django.contrib.auth.models import User

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

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario o email', max_length=150, widget=forms.TextInput(attrs={'placeholder':'usuario o email'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label='Nombre', required=False)
    email = forms.EmailField(label='Correo', required=True)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email:
            raise ValidationError('Introduce un email válido que contenga @')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Ya existe un usuario con ese correo')
        return email

    def clean_password1(self):
        p = self.cleaned_data.get('password1')
        if not p or len(p) < 10:
            raise ValidationError('La contraseña debe tener al menos 10 caracteres')
        return p

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if not p2:
            raise ValidationError({'password2': 'Debes confirmar la contraseña'})
        if p1 and p2 and p1 != p2:
            raise ValidationError('Las contraseñas no coinciden')
        return cleaned

    def save(self, commit=True):
        # leave user creation to view
        user = User()
        user.username = self.cleaned_data.get('username') or self.cleaned_data.get('email')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.set_password(self.cleaned_data.get('password1'))
            user.save()
        return user

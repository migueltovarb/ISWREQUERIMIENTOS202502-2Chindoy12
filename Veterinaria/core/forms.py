from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Pet, Appointment, Certificate
from django.utils import timezone


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'birth_date']


class AppointmentForm(forms.ModelForm):
    start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Appointment
        fields = ['pet', 'veterinarian', 'type', 'start', 'end', 'notes']

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start')
        end = cleaned.get('end')
        if start and end and end <= start:
            raise forms.ValidationError('La hora de fin debe ser posterior a la hora de inicio')
        return cleaned


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['pet', 'client_name', 'content']

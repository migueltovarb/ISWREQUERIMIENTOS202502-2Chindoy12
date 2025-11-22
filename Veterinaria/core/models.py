from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Usuario personalizado para la app.

    Mantener como `core.User` y usar `AUTH_USER_MODEL = 'core.User'` en settings.
    """
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('vet', 'Veterinario'),
        ('client', 'Cliente'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')


class Pet(models.Model):
    owner = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50, blank=True)
    breed = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.owner.username})"


class Appointment(models.Model):
    TYPE_CHOICES = (
        ('control', 'Control'),
        ('vacunacion', 'Vacunación'),
        ('cirugia', 'Cirugía'),
        ('consulta', 'Consulta general'),
    )
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='appointments')
    veterinarian = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments_as_vet')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    start = models.DateTimeField()
    end = models.DateTimeField()
    notes = models.TextField(blank=True)
    cancelled = models.BooleanField(default=False)

    class Meta:
        ordering = ['start']

    def __str__(self):
        return f"{self.pet.name} - {self.type} @ {self.start}"


class Vaccine(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class MedicalRecord(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='medical_records')
    created_by = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"Record {self.id} - {self.pet.name}"


class Certificate(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='certificates')
    client_name = models.CharField(max_length=200)
    content = models.TextField()
    issued_at = models.DateTimeField(auto_now_add=True)
    veterinarian = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, related_name='issued_certificates')
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True)

    def __str__(self):
        return f"Certificado {self.id} - {self.pet.name}"


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=[
        ('cliente', 'Cliente'),
        ('veterinario', 'Veterinario'),
    ], default='cliente')

    def __str__(self):
        return f"{self.user.username} - {self.rol}"

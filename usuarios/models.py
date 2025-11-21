from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError


class Perfil(models.Model):
    ROLES = [
        ('cliente', 'Cliente'),
        ('veterinario', 'Veterinario'),
        ('administrador', 'Administrador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"


class Mascota(models.Model):
    SEXO = [('M', 'Macho'), ('H', 'Hembra')]

    propietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mascotas')
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50, blank=True)
    raza = models.CharField(max_length=50, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=SEXO, blank=True)
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.propietario.username})"


class Vacuna(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    fabricante = models.CharField(max_length=150, blank=True)
    dosis = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.nombre


class HistorialMedico(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='historiales')
    fecha = models.DateTimeField(default=timezone.now)
    descripcion = models.TextField()
    diagnostico = models.TextField(blank=True)
    tratamiento = models.TextField(blank=True)
    veterinario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='atenciones')
    vacunas = models.ManyToManyField(Vacuna, blank=True, related_name='historiales')

    def __str__(self):
        return f"Historial {self.mascota.nombre} @ {self.fecha.date()}"


class Cita(models.Model):
    TIPO = [
        ('control', 'Control'),
        ('vacunacion', 'Vacunación'),
        ('cirugia', 'Cirugía'),
        ('consulta_general', 'Consulta general'),
    ]
    ESTADO = [
        ('programada', 'Programada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]

    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='citas')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='citas_cliente')
    veterinario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='citas_veterinario')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    tipo = models.CharField(max_length=20, choices=TIPO, default='consulta_general')
    estado = models.CharField(max_length=20, choices=ESTADO, default='programada')
    motivo = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"Cita {self.mascota.nombre} - {self.tipo} @ {self.fecha_inicio}"

    def clean(self):
        # Validaciones básicas
        if self.fecha_fin <= self.fecha_inicio:
            raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')

        # Evitar solapamiento para el mismo veterinario
        if self.veterinario:
            qs = Cita.objects.filter(veterinario=self.veterinario, estado='programada')
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            overlap = qs.filter(fecha_inicio__lt=self.fecha_fin, fecha_fin__gt=self.fecha_inicio).exists()
            if overlap:
                raise ValidationError('El veterinario tiene otra cita en ese horario.')

        # Evitar solapamiento para la misma mascota
        qs2 = Cita.objects.filter(mascota=self.mascota, estado='programada')
        if self.pk:
            qs2 = qs2.exclude(pk=self.pk)
        overlap2 = qs2.filter(fecha_inicio__lt=self.fecha_fin, fecha_fin__gt=self.fecha_inicio).exists()
        if overlap2:
            raise ValidationError('La mascota ya tiene otra cita en ese horario.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Certificado(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificados')
    vacunacion = models.ForeignKey(Vacuna, on_delete=models.SET_NULL, null=True, blank=True)
    tratamiento = models.TextField(blank=True)
    fecha_emision = models.DateTimeField(default=timezone.now)
    veterinario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='certificados_emitidos')
    archivo_pdf = models.FileField(upload_to='certificados/', blank=True, null=True)
    codigo_qr = models.ImageField(upload_to='certificados/qr/', blank=True, null=True)

    def __str__(self):
        return f"Certificado {self.mascota.nombre} - {self.fecha_emision.date()}"


class Estadistica(models.Model):
    mascota = models.OneToOneField(Mascota, on_delete=models.CASCADE, related_name='estadistica', null=True, blank=True)
    total_vacunas = models.PositiveIntegerField(default=0)
    total_consultas = models.PositiveIntegerField(default=0)
    total_tratamientos = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.mascota:
            return f"Estadística {self.mascota.nombre}"
        return "Estadística general"


# Señales para crear perfil automáticamente
@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)


@receiver(post_save, sender=User)
def guardar_perfil(sender, instance, **kwargs):
    # Asegura que existe el perfil y lo guarda
    try:
        perfil = instance.perfil
        perfil.save()
    except Perfil.DoesNotExist:
        Perfil.objects.create(user=instance)


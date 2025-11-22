from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # Root -> mostrar login primero
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    # Home redirige según rol después de autenticarse
    path('home/', views.dashboard_redirect, name='home'),
    path('dashboard_admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard_cliente/', views.dashboard_cliente, name='dashboard_cliente'),
    path('dashboard_veterinario/', views.dashboard_veterinario, name='dashboard_veterinario'),
    # Cliente
    path('mis-mascotas/', views.mis_mascotas, name='mis_mascotas'),
    path('agendar-cita/', views.agendar_cita, name='agendar_cita'),
    path('historial-citas/', views.historial_citas, name='historial_citas'),
    path('mis-certificados/', views.mis_certificados, name='mis_certificados'),
    # Veterinario
    path('citas-programadas/', views.citas_programadas, name='citas_programadas'),
    path('historial-clinico/', views.historial_clinico, name='historial_clinico'),
    path('mascotas-vet/', views.mascotas_vet, name='mascotas_vet'),
    path('emitir-certificado/', views.emitir_certificado, name='emitir_certificado'),

    # Pets
    path('pets/', views.my_pets, name='my_pets'),
    path('pets/new/', views.pet_create, name='pet_create'),

    # Appointments
    path('appointments/', views.my_appointments, name='my_appointments'),
    path('appointments/new/', views.schedule_appointment, name='schedule_appointment'),

    # Certificates
    path('certificates/', views.certificates_list, name='certificates_list'),
    path('certificates/new/', views.emit_certificate, name='emit_certificate'),

    # Admin management
    path('admin/users/', views.admin_users_manage, name='admin_users_manage'),
    path('admin/appointments/', views.admin_appointments_view, name='admin_appointments_view'),
]

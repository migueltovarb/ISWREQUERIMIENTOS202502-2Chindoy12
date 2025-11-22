from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import RegisterForm, PetForm, AppointmentForm, CertificateForm
from .models import Pet, Appointment, Certificate, User, MedicalRecord, Perfil
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages



def get_perfil(user):
    try:
        return Perfil.objects.get(user=user)
    except Perfil.DoesNotExist:
        return None


def dashboard_redirect(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_superuser:
        return redirect('dashboard_admin')
    perfil = get_perfil(request.user)
    if perfil:
        if perfil.rol == 'cliente':
            return redirect('dashboard_cliente')
        elif perfil.rol == 'veterinario':
            return redirect('dashboard_veterinario')
    # fallback to user.role if Perfil missing
    if hasattr(request.user, 'role'):
        if request.user.role == 'vet':
            return redirect('dashboard_veterinario')
        if request.user.role == 'admin':
            return redirect('dashboard_admin')
    return redirect('login')


@login_required
def dashboard_admin(request):
    UserModel = get_user_model()
    usuarios = UserModel.objects.filter(is_superuser=False)
    perfiles = Perfil.objects.filter(user__in=usuarios)
    tabla = []
    for perfil in perfiles:
        tabla.append({
            'id': perfil.id,
            'username': perfil.user.username,
            'email': perfil.user.email,
            'rol': perfil.rol,
        })
    if request.method == 'POST':
        perfil_id = request.POST.get('perfil_id')
        nuevo_rol = request.POST.get('nuevo_rol')
        perfil = Perfil.objects.get(id=perfil_id)
        perfil.rol = nuevo_rol
        perfil.save()
        return redirect('dashboard_admin')
    return render(request, 'dashboard_admin.html', {'tabla': tabla})


@login_required
def dashboard_cliente(request):
    return render(request, 'dashboard_cliente.html')


@login_required
def dashboard_veterinario(request):
    return render(request, 'dashboard_veterinario.html')


# --- Authentication views (basic) ---
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # create Perfil for the user
            Perfil.objects.get_or_create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('login')


# Cliente views
@login_required
def mis_mascotas(request):
    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'mis_mascotas.html', {'pets': pets})


@login_required
def agendar_cita(request):
    # reuse schedule_appointment logic if needed
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            if appt.pet.owner != request.user:
                messages.error(request, 'La mascota seleccionada no te pertenece')
            else:
                appt.save()
                return redirect('mis_mascotas')
    else:
        form = AppointmentForm()
        form.fields['pet'].queryset = Pet.objects.filter(owner=request.user)
    return render(request, 'agendar_cita.html', {'form': form})


@login_required
def historial_citas(request):
    return render(request, 'historial_citas.html')


@login_required
def mis_certificados(request):
    certs = Certificate.objects.filter(pet__owner=request.user)
    return render(request, 'mis_certificados.html', {'certificates': certs})


# Veterinario views
@login_required
def citas_programadas(request):
    appts = Appointment.objects.filter(veterinarian=request.user).order_by('start')
    return render(request, 'citas_programadas.html', {'appointments': appts})


@login_required
def historial_clinico(request):
    return render(request, 'historial_clinico.html')


@login_required
def mascotas_vet(request):
    return render(request, 'mascotas_vet.html')


@login_required
def emitir_certificado(request):
    # present form to create certificate
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.veterinarian = request.user
            cert.save()
            return redirect('mis_certificados')
    else:
        form = CertificateForm()
    return render(request, 'emitir_certificado.html', {'form': form})


# Aliases / existing names used elsewhere
def certificates_list(request):
    if request.user.is_superuser:
        certs = Certificate.objects.all()
    elif get_perfil(request.user) and get_perfil(request.user).rol == 'veterinario':
        certs = Certificate.objects.filter(veterinarian=request.user)
    else:
        certs = Certificate.objects.filter(pet__owner=request.user)
    return render(request, 'certificates_list.html', {'certificates': certs})


def emit_certificate(request):
    return emitir_certificado(request)


@login_required
def my_pets(request):
    return mis_mascotas(request)


@login_required
def pet_create(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            return redirect('mis_mascotas')
    else:
        form = PetForm()
    return render(request, 'pet_form.html', {'form': form})


@login_required
def my_appointments(request):
    if get_perfil(request.user) and get_perfil(request.user).rol == 'veterinario':
        appts = Appointment.objects.filter(veterinarian=request.user).order_by('-start')
    else:
        appts = Appointment.objects.filter(pet__owner=request.user).order_by('-start')
    return render(request, 'appointments_list.html', {'appointments': appts})


@login_required
def schedule_appointment(request):
    return agendar_cita(request)


@login_required
def admin_users_manage(request):
    UserModel = get_user_model()
    usuarios = UserModel.objects.filter(is_superuser=False)
    perfiles = Perfil.objects.filter(user__in=usuarios)
    if request.method == 'POST':
        perfil_id = request.POST.get('perfil_id')
        nuevo_rol = request.POST.get('nuevo_rol')
        perfil = Perfil.objects.get(id=perfil_id)
        perfil.rol = nuevo_rol
        perfil.save()
        return redirect('dashboard_admin')
    tabla = []
    for perfil in perfiles:
        tabla.append({'id': perfil.id, 'username': perfil.user.username, 'email': perfil.user.email, 'rol': perfil.rol})
    return render(request, 'admin_users.html', {'users': tabla})


@login_required
def admin_appointments_view(request):
    qs = Appointment.objects.all()
    day = request.GET.get('day')
    month = request.GET.get('month')
    year = request.GET.get('year')
    if day and month and year:
        qs = qs.filter(start__year=int(year), start__month=int(month), start__day=int(day))
    elif month and year:
        qs = qs.filter(start__year=int(year), start__month=int(month))
    return render(request, 'admin_appointments.html', {'appointments': qs})


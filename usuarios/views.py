from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import RegistroForm, MascotaForm, CitaForm
from .models import Perfil, Mascota, Cita, HistorialMedico, Vacuna
from django.contrib import messages

# ---------------------------
# Registro con LOGIN automático
# ---------------------------
def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            perfil = Perfil.objects.create(user=user)

            # Iniciar sesión
            usuario = authenticate(username=user.username, password=form.cleaned_data["password"])
            login(request, usuario)

            return redirect("dashboard")
    else:
        form = RegistroForm()
    return render(request, "registro.html", {"form": form})

# ---------------------------
# Dashboard general
# ---------------------------
@login_required
def dashboard(request):
    rol = request.user.perfil.rol

    if request.user.is_staff:
        return redirect("dashboard_admin")

    if rol == "veterinario":
        return redirect("dashboard_veterinario")

    return redirect("dashboard_cliente")


# ---------------------------
# Dashboard CLIENTE
# ---------------------------
@login_required
def dashboard_cliente(request):
    return render(request, "dash_cliente.html")


# ---------------------------
# Mascotas
# ---------------------------
@login_required
def lista_mascotas(request):
    mascotas = Mascota.objects.filter(propietario=request.user)
    return render(request, "lista_mascotas.html", {"mascotas": mascotas})


@login_required
def crear_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.propietario = request.user
            mascota.save()
            messages.success(request, 'Mascota registrada correctamente')
            return redirect('lista_mascotas')
    else:
        form = MascotaForm()
    return render(request, 'mascota_form.html', {'form': form})


@login_required
def detalle_mascota(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk, propietario=request.user)
    historiales = mascota.historiales.all()
    return render(request, 'detalle_mascota.html', {'mascota': mascota, 'historiales': historiales})


# ---------------------------
# Citas
# ---------------------------
@login_required
def lista_citas(request):
    # Clientes ven sus citas; veterinarios ven las suyas
    if request.user.perfil.rol == 'veterinario':
        citas = Cita.objects.filter(veterinario=request.user)
    else:
        citas = Cita.objects.filter(cliente=request.user)
    return render(request, 'lista_citas.html', {'citas': citas})


@login_required
def crear_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.cliente = request.user
            cita.save()
            messages.success(request, 'Cita programada correctamente')
            return redirect('lista_citas')
    else:
        form = CitaForm()
        # limitar mascotas al cliente
        form.fields['mascota'].queryset = Mascota.objects.filter(propietario=request.user)
    return render(request, 'cita_form.html', {'form': form})


@login_required
def cancelar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    # permitir cancelar si es cliente dueño o admin/veterinario
    if request.user == cita.cliente or request.user.is_staff or request.user == cita.veterinario:
        cita.estado = 'cancelada'
        cita.save()
        messages.success(request, 'Cita cancelada')
    return redirect('lista_citas')


@login_required
def editar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            cita = form.save()
            messages.success(request, 'Cita actualizada')
            return redirect('lista_citas')
    else:
        form = CitaForm(instance=cita)
        form.fields['mascota'].queryset = Mascota.objects.filter(propietario=cita.cliente)
    return render(request, 'cita_form.html', {'form': form, 'editar': True})


# ---------------------------
# Dashboard VETERINARIO
# ---------------------------
@login_required
def dashboard_veterinario(request):
    return render(request, "dash_veterinario.html")


# ---------------------------
# Dashboard ADMIN
# ---------------------------
@login_required
@user_passes_test(lambda u: u.is_staff)
def dashboard_admin(request):
    usuarios = Perfil.objects.all()
    return render(request, "dash_admin.html", {"usuarios": usuarios})

# ---------------------------
# Cambiar ROL (admin)
# ---------------------------
@login_required
@user_passes_test(lambda u: u.is_staff)
def cambiar_rol(request, id, nuevo_rol):
    perfil = Perfil.objects.get(id=id)
    perfil.rol = nuevo_rol
    perfil.save()
    return redirect("dashboard_admin")

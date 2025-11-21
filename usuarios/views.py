from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import RegistroForm
from .models import Perfil

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

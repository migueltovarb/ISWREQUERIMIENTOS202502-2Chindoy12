from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from .forms import RegisterForm, LoginForm
from core.models import Perfil
from django.contrib import messages

User = get_user_model()


def is_admin(user):
    return user.is_superuser


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # redirect according to role
                try:
                    perfil = Perfil.objects.get(user=user)
                    rol = perfil.rol
                except Perfil.DoesNotExist:
                    rol = getattr(user, 'role', None)
                if user.is_superuser or rol == 'admin' or getattr(user, 'role', None) == 'admin':
                    return redirect('dashboard_admin')
                if rol == 'veterinario' or getattr(user, 'role', None) == 'vet':
                    return redirect('dashboard_veterinario')
                return redirect('dashboard_cliente')
            else:
                messages.error(request, 'Usuario o contraseña inválidos')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('username') or form.cleaned_data.get('email')
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password1'])
            user.save()
            # ensure Perfil exists and default role 'cliente'
            Perfil.objects.get_or_create(user=user, defaults={'rol': 'cliente'})
            login(request, user)
            return redirect('dashboard_cliente')
    else:
        form = RegisterForm()
    return render(request, 'usuarios/register.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    usuarios = User.objects.filter(is_superuser=False)
    perfiles = Perfil.objects.filter(user__in=usuarios).select_related('user')
    if request.method == 'POST':
        perfil_id = request.POST.get('perfil_id')
        nuevo_rol = request.POST.get('nuevo_rol')
        perfil = get_object_or_404(Perfil, id=perfil_id)
        # admin cannot change their own role
        if perfil.user == request.user:
            messages.error(request, 'No puedes cambiar tu propio rol')
        else:
            if nuevo_rol in ['cliente', 'veterinario']:
                perfil.rol = nuevo_rol
                perfil.save()
                messages.success(request, f"Rol de {perfil.user.username} cambiado a {nuevo_rol}")
        return redirect('admin_panel')
    # build table data
    tabla = []
    for p in perfiles:
        tabla.append({'id': p.id, 'username': p.user.username, 'email': p.user.email, 'rol': p.rol})
    return render(request, 'usuarios/admin_panel.html', {'tabla': tabla})


@login_required
def profile_redirect(request):
    # helper to redirect logged users to their dashboard
    user = request.user
    if user.is_superuser:
        return redirect('dashboard_admin')
    try:
        perfil = Perfil.objects.get(user=user)
        rol = perfil.rol
    except Perfil.DoesNotExist:
        rol = getattr(user, 'role', None)
    if rol == 'veterinario' or getattr(user, 'role', None) == 'vet':
        return redirect('dashboard_veterinario')
    return redirect('dashboard_cliente')

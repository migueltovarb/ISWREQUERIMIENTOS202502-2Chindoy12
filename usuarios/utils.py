from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def role_required(rol):
    """Decorador simple que verifica `request.user.perfil.rol`.
    Si no está autenticado redirige a login; si no tiene rol devuelve 403.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            try:
                user_rol = request.user.perfil.rol
            except Exception:
                return HttpResponseForbidden('Perfil no configurado')
            if user_rol != rol and not request.user.is_staff:
                return HttpResponseForbidden('Acceso denegado')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def roles_required(roles):
    """Permite varios roles (lista)."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            try:
                user_rol = request.user.perfil.rol
            except Exception:
                return HttpResponseForbidden('Perfil no configurado')
            if user_rol not in roles and not request.user.is_staff:
                return HttpResponseForbidden('Acceso denegado')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator

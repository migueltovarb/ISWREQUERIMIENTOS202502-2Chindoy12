from django.shortcuts import redirect

def veterinario_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.perfil.rol == "veterinario":
            return view_func(request, *args, **kwargs)
        return redirect("/")
    return _wrapped

from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from .forms import RegistroForm

class RegistroView(FormView):
    template_name = "registro.html"
    form_class = RegistroForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        usuario = User.objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"]
        )

        # Email de bienvenida
        mensaje = f"""
Hola {usuario.username},

¡Bienvenido a la Veterinaria!

Tu registro se completó correctamente.
"""
        send_mail(
            subject="Registro exitoso - Veterinaria",
            message=mensaje,
            from_email="veterinaria@gmail.com",
            recipient_list=[usuario.email],
            fail_silently=False,
        )

        return super().form_valid(form)


class LoginUsuario(LoginView):
    template_name = "login.html"

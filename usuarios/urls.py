from django.urls import path
from .views import RegistroView, LoginUsuario

urlpatterns = [
    path("login/", LoginUsuario.as_view(), name="login"),
    path("registro/", RegistroView.as_view(), name="registro"),
]

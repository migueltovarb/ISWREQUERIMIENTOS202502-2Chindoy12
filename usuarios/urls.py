from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("registro/", views.registro, name="registro"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # dashboards según rol
    path("dashboard-cliente/", views.dashboard_cliente, name="dashboard_cliente"),
    path("dashboard-veterinario/", views.dashboard_veterinario, name="dashboard_veterinario"),
    path("dashboard-admin/", views.dashboard_admin, name="dashboard_admin"),

    # cambio de rol
    path("cambiar-rol/<int:id>/<str:nuevo_rol>/", views.cambiar_rol, name="cambiar_rol"),
]

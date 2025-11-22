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
    # Mascotas
    path('mascotas/', views.lista_mascotas, name='lista_mascotas'),
    path('mascotas/nueva/', views.crear_mascota, name='crear_mascota'),
    path('mascotas/<int:pk>/', views.detalle_mascota, name='detalle_mascota'),

    # Citas
    path('citas/', views.lista_citas, name='lista_citas'),
    path('citas/nueva/', views.crear_cita, name='crear_cita'),
    path('citas/<int:pk>/editar/', views.editar_cita, name='editar_cita'),
    path('citas/<int:pk>/cancelar/', views.cancelar_cita, name='cancelar_cita'),
]

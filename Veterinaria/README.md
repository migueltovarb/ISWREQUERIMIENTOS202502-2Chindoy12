# Veterinaria (Django)

Proyecto Django mínimo para gestión de una clínica veterinaria.

Pasos iniciales:

1. Activar tu entorno virtual (ya lo tienes creado).
2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3. Crear migraciones y migrar:

```powershell
python manage.py makemigrations
python manage.py migrate
```

4. Crear superusuario (administrador):

```powershell
python manage.py createsuperuser
```

5. Ejecutar servidor de desarrollo:

```powershell
python manage.py runserver
```

Notas:
- Configura en `veterinaria_project/settings.py` las credenciales SMTP para enviar correos (Gmail).
- El login tiene botón de modo oscuro y enlace a registro.

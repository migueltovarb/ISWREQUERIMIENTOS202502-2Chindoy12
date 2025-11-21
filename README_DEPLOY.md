# Instrucciones rápidas para ejecutar localmente y preparar despliegue

Requisitos mínimos:
- Python 3.10+
- Virtualenv

Pasos para ejecutar localmente (PowerShell):

1. Crear y activar entorno:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias:
```powershell
pip install -r requirements.txt
```

3. Variables de entorno (usar `.env` o exportarlas):
```
SECRET_KEY=tu_secret_key_segura
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

4. Migraciones y static:
```powershell
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

5. Ejecutar servidor de desarrollo:
```powershell
python manage.py runserver
```

Para producción recomiendo usar Docker, Gunicorn + Nginx y Postgres. Consulta el archivo `requirements.txt` para librerías sugeridas.

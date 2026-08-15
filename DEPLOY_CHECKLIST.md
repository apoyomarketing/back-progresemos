# Checklist de configuración para deploy en Dokploy (VPS Contabo)

Auditoría del estado actual del backend (`back-progresemos`, Django + DRF) para desplegarlo en Dokploy vía Dockerfile. Estado actual: deploy solo por IP (`169.58.180.28`), sin dominio todavía, mismo origen para front/back (sin CORS por ahora).

---

## 1. Bloqueantes (rompen el deploy o dejan la API inutilizable)

### 1.1 `api/` no está conectado a ninguna URL
`config/urls.py` solo tiene:
```python
urlpatterns = [
    path('admin/', admin.site.urls),
]
```
La app `api` no tiene `urls.py` propio y no está incluida aquí. Resultado: **ningún endpoint de la API responde**, solo `/admin/`. Hay que crear `api/urls.py` con las rutas del proyecto e incluirlo en `config/urls.py`:
```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

### 1.2 `CSRF_TRUSTED_ORIGINS` vacío
En `.env`:
```
CSRF_TRUSTED_ORIGINS=
```
Con `DEBUG=False`, cualquier POST/PUT/DELETE autenticado por cookie (incluido el login del admin) va a fallar con 403 en cuanto se acceda por un origen no confiable. Como mínimo, mientras se usa la IP:
```
CSRF_TRUSTED_ORIGINS=http://169.58.180.28
```

### 1.3 Confirmar cómo llegan las env vars de la DB dentro de Dokploy
`.env` tiene `DB_HOST=despliegue-db-h900sg`, que es un nombre de servicio interno típico de Dokploy (probablemente ya creaste un servicio Postgres ahí). Verificar en el panel de Dokploy:
- Que la app y la base de datos estén en la **misma red interna** del proyecto.
- Que las variables `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` estén cargadas como **variables de entorno de la app en Dokploy** (no dependas de que el archivo `.env` viaje dentro de la imagen — `settings.py` usa `load_dotenv()`, que si no encuentra `.env` simplemente no hace nada y cae en `os.environ`, así que las env vars puestas en el dashboard de Dokploy sí van a funcionar).

### 1.4 Commitear el cambio de SQLite → Postgres
`config/settings.py` y `requirements.txt` tienen cambios sin commitear (working tree):
- `DATABASES` pasó de `sqlite3` a `postgresql` leyendo `DB_NAME/DB_USER/DB_PASSWORD/DB_HOST/DB_PORT`.
- Se agregó `psycopg2-binary` a `requirements.txt`.

Si Dokploy hace `git pull` + build desde el repo remoto, **este cambio no existe en el remoto todavía** y el deploy va a intentar usar SQLite (o fallar por el import de `psycopg2`). Hay que revisar, commitear y pushear estos dos archivos antes de desplegar.

---

## 2. Configurar ahora (deploy solo por IP)

Variables de entorno a definir en el panel de Dokploy (Environment del servicio):

| Variable | Valor sugerido | Nota |
|---|---|---|
| `SECRET_KEY` | la clave generada antes (`vvfu(77q9g...`) | No usar el fallback hardcodeado de `settings.py` |
| `DEBUG` | `False` | Ya está así en tu `.env` |
| `ALLOWED_HOSTS` | `169.58.180.28` | Ya está así |
| `CSRF_TRUSTED_ORIGINS` | `http://169.58.180.28` | Está vacío hoy, ver 1.2 |
| `DB_NAME` / `DB_USER` / `DB_PASSWORD` / `DB_HOST` / `DB_PORT` | valores del servicio Postgres de Dokploy | Ya están en tu `.env` |
| `SECURE_SSL_REDIRECT` | `False` | Correcto mientras no haya HTTPS propio; si Dokploy/Traefik ya redirige a HTTPS a nivel de proxy, dejar en `False` evita loops de redirect en Django |

Nada más es estrictamente necesario para levantar el contenedor con la IP actual, **una vez resueltos los bloqueantes de la sección 1**.

---

## 3. Cuando compren el dominio (y subdominios)

1. **`ALLOWED_HOSTS`**: agregar el dominio y subdominios, ej. `ALLOWED_HOSTS=169.58.180.28,api.progresemos.com`.
2. **`CSRF_TRUSTED_ORIGINS`**: agregar el origen completo con esquema, ej. `CSRF_TRUSTED_ORIGINS=https://api.progresemos.com`.
3. **CORS**: si el frontend queda en un subdominio distinto al backend (ej. `app.progresemos.com` llamando a `api.progresemos.com`), eso ya es cross-origin desde el navegador. Hoy no hay nada de CORS instalado. Vas a necesitar:
   ```
   pip install django-cors-headers
   ```
   y en `settings.py`:
   ```python
   INSTALLED_APPS += ['corsheaders']
   MIDDLEWARE.insert(0 o después de SecurityMiddleware, 'corsheaders.middleware.CorsMiddleware')
   CORS_ALLOWED_ORIGINS = ['https://app.progresemos.com']
   ```
4. **HTTPS real**: una vez que Dokploy/Traefik emita el certificado Let's Encrypt para el dominio:
   - `SECURE_SSL_REDIRECT=True`
   - Agregar en `settings.py` (falta hoy): `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')` — sin esto, Django no sabe que Traefik ya terminó el SSL y puede entrar en loop de redirección al forzar `SECURE_SSL_REDIRECT`.
   - Considerar `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS` (dado que van a tener subdominios), `SECURE_HSTS_PRELOAD`.

---

## 4. Bugs de código a corregir (no bloquean pero están rotos)

- **Email mal configurado**: `settings.py` define un diccionario `MAILERS`, que **no es una setting real de Django**. Django ignora esto por completo y usa el backend SMTP por defecto apuntando a `localhost:25`, que va a fallar. Corregir a:
  ```python
  EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
  EMAIL_HOST = os.environ.get('EMAIL_HOST')
  EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
  EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
  EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
  EMAIL_USE_TLS = True
  ```
  (o dejar `console.EmailBackend` explícitamente si por ahora no se envían correos).

- **`SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE` comparten la misma env var** (`SECURE_SSL_REDIRECT`). Cuando actives HTTPS vas a querer separarlas para tener control fino, aunque en la práctica activarlas juntas también es válido.

- **`.pyc` trackeados en git**: `config/__pycache__/*.pyc` están commiteados desde el primer commit (antes de que existiera `.gitignore`), incluido el bytecode de `settings.py`, que contiene compilado el `SECRET_KEY` insecure-default hardcodeado como fallback. No es tu secreto de producción real, pero conviene sacarlo del repo:
  ```
  git rm -r --cached config/__pycache__
  ```

- **`.env.example` desactualizado**: todavía documenta `DB_PATH` (de cuando era SQLite) en vez de `DB_NAME/DB_USER/DB_PASSWORD/DB_HOST/DB_PORT`, y usa la IP real como si fuera un placeholder. Actualizarlo ayuda a que cualquier otra persona que clone el repo sepa qué variables necesita.

---

## 5. Recomendado pero no bloqueante

- **Healthcheck**: no existe ni un endpoint `/health` ni una instrucción `HEALTHCHECK` en el `Dockerfile`. Dokploy lo usa para saber si el deploy está sano antes de cortar tráfico al contenedor anterior. Sugerido:
  ```python
  # api/urls.py
  path('health/', lambda request: HttpResponse('ok')),
  ```
  ```dockerfile
  HEALTHCHECK CMD curl -f http://localhost:8000/health/ || exit 1
  ```
- **`MEDIA_URL` / `MEDIA_ROOT`**: no están definidos. Hoy no hay modelos con `FileField`/`ImageField`, pero el día que agregues uploads esto va a romper. Definirlos (y pensar si los archivos van a un volumen o a almacenamiento externo tipo S3) antes de necesitarlo.
- **Logging**: no hay `LOGGING` configurado, usa el default de Django (va a stdout/stderr, que Docker/Dokploy capturan igual, así que no es urgente).
- **Monitoreo de errores**: no hay Sentry ni nada similar. Útil para enterarte de 500s en producción sin revisar logs a mano.
- **Gunicorn**: agregar `--access-logfile -` en `entrypoint.sh` para que los logs de acceso salgan por stdout y los veas en Dokploy.
- **Pin de versión de Python**: `Dockerfile` usa `python:3.12-slim` (flotante a la última patch de 3.12). Pinéalo a una versión exacta si querés reproducibilidad de builds.
- **`README.md`** está vacío (una sola línea). No es necesario para el deploy pero ayuda a cualquiera que retome el proyecto.
